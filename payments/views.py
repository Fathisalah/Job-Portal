from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Payment
from jobs.models import Job, JobApplication

@login_required
def payment_process(request, job_id):
    job = get_object_or_404(Job, id=job_id)
    
    # Create payment record
    payment = Payment.objects.create(
        user=request.user,
        job=job,
        amount=job.application_fee
    )
    
    if request.method == 'POST':
        # Simulate payment success (in real app, integrate with payment gateway)
        payment.status = 'completed'
        payment.transaction_id = f'TRANS_{payment.id}'
        payment.save()
        
        # Create job application after payment
        JobApplication.objects.create(
            job=job,
            applicant=request.user.userprofile,
            status='pending'
        )
        
        messages.success(request, 'Payment successful! Your application has been submitted.')
        return redirect('job_list')
    
    return render(request, 'payments/payment_process.html', {
        'payment': payment,
        'job': job
    })

@login_required
def payment_history(request):
    payments = Payment.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'payments/payment_history.html', {'payments': payments}) 