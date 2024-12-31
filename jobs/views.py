from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Job, JobApplication
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings

@login_required
def job_list(request):
    context = {
        'is_employer': request.user.userprofile.is_employer
    }
    
    if context['is_employer']:
        # For employers, show their posted jobs
        context['jobs'] = Job.objects.filter(employer=request.user.userprofile).order_by('-created_at')
    else:
        # For job seekers, show ALL jobs without filtering by is_active
        jobs = Job.objects.all().order_by('-created_at')
        
        # Add application status to each job
        for job in jobs:
            try:
                application = JobApplication.objects.get(job=job, applicant=request.user.userprofile)
                job.application_status = application.get_status_display()
                job.application_status_color = application.get_status_badge_color()
            except JobApplication.DoesNotExist:
                job.application_status = None
        
        context['jobs'] = jobs
    
    return render(request, 'jobs/job_list.html', context)

@login_required
def post_job(request):
    if not request.user.userprofile.is_employer:
        messages.error(request, 'Only employers can post jobs.')
        return redirect('job_list')
        
    if request.method == 'POST':
        job = Job.objects.create(
            employer=request.user.userprofile,
            title=request.POST.get('title'),
            description=request.POST.get('description'),
            requirements=request.POST.get('requirements'),
            location=request.POST.get('location'),
            salary=request.POST.get('salary'),
            application_fee=request.POST.get('application_fee', 0),
            is_active=True
        )
        messages.success(request, 'Job posted successfully!')
        return redirect('job_list')
        
    return render(request, 'jobs/post_job.html')

@login_required
def apply_job(request, job_id):
    job = get_object_or_404(Job, id=job_id)
    
    if request.user.userprofile.is_employer:
        messages.error(request, 'Employers cannot apply for jobs.')
        return redirect('job_list')
        
    if JobApplication.objects.filter(job=job, applicant=request.user.userprofile).exists():
        messages.warning(request, 'You have already applied for this job.')
        return redirect('job_list')
        
    if request.method == 'POST':
        # Create application without requiring cover letter
        JobApplication.objects.create(
            job=job,
            applicant=request.user.userprofile,
            status='pending'
        )
        messages.success(request, 'Application submitted successfully!')
        return redirect('job_list')
        
    return render(request, 'jobs/job_detail.html', {'job': job})

@login_required
def job_detail(request, job_id):
    job = get_object_or_404(Job, id=job_id)
    has_applied = JobApplication.objects.filter(
        job=job, 
        applicant=request.user.userprofile
    ).exists()
    
    context = {
        'job': job,
        'has_applied': has_applied
    }
    return render(request, 'jobs/job_detail.html', context)

@login_required
def employer_dashboard(request):
    if not request.user.userprofile.is_employer:
        messages.error(request, 'Access denied. Employer account required.')
        return redirect('job_list')
    
    # Get all jobs posted by the employer
    jobs = Job.objects.filter(employer=request.user.userprofile).order_by('-created_at')
    applications = JobApplication.objects.filter(job__employer=request.user.userprofile).order_by('-applied_at')
    
    context = {
        'jobs': jobs,
        'applications': applications,
        'status_choices': JobApplication.STATUS_CHOICES,
    }
    return render(request, 'jobs/employer_dashboard.html', context)

@login_required
def update_application_status(request, application_id):
    if not request.user.userprofile.is_employer:
        messages.error(request, 'Access denied. Employer account required.')
        return redirect('job_list')
    
    application = get_object_or_404(JobApplication, id=application_id)
    
    # Verify the employer owns this job
    if application.job.employer != request.user.userprofile:
        messages.error(request, 'Access denied. Not your job posting.')
        return redirect('employer_dashboard')
    
    if request.method == 'POST':
        new_status = request.POST.get('status')
        if new_status in dict(JobApplication.STATUS_CHOICES):
            old_status = application.status
            application.status = new_status
            application.save()
            
            # Send notification message
            messages.success(request, f'Application status updated from {old_status} to {new_status}')
            
            # Update the applicant's view immediately
            try:
                subject = f'Job Application Status Update - {application.job.title}'
                message = f'''
                Dear {application.applicant.user.get_full_name()},
                
                Your application for the position of {application.job.title} has been updated.
                
                New Status: {new_status}
                
                You can check the details in your job portal.
                
                Best regards,
                {application.job.employer.company_name}
                '''
                application.applicant.user.email_user(subject, message)
            except Exception as e:
                print(f"Email sending failed: {str(e)}")
    
    return redirect('employer_dashboard') 