from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth import login, authenticate, logout
from .models import UserProfile
from django.contrib.auth.models import User

def login_view(request):
    # Always show login page first, even for authenticated users
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            messages.success(request, f'Welcome back, {username}!')
            return redirect('job_list')
        else:
            messages.error(request, 'Invalid username or password.')
    
    return render(request, 'accounts/login.html')

def register(request):
    if request.user.is_authenticated:
        return redirect('job_list')
        
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
        is_employer = request.POST.get('is_employer') == 'on'
        
        if password != confirm_password:
            messages.error(request, 'Passwords do not match.')
            return redirect('register')
            
        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username already exists.')
            return redirect('register')
            
        user = User.objects.create_user(username=username, email=email, password=password)
        UserProfile.objects.create(user=user, is_employer=is_employer)
        
        login(request, user)
        messages.success(request, 'Registration successful!')
        return redirect('job_list')
        
    return render(request, 'accounts/register.html')

def logout_view(request):
    logout(request)
    messages.info(request, 'You have been logged out.')
    return redirect('login')

@login_required
def update_profile(request):
    user = request.user
    profile = user.userprofile
    
    if request.method == 'POST':
        # Update User model fields
        user.first_name = request.POST.get('first_name')
        user.last_name = request.POST.get('last_name')
        user.email = request.POST.get('email')
        user.save()
        
        # Update UserProfile fields
        profile.phone_number = request.POST.get('phone_number')
        profile.address = request.POST.get('address')
        if request.POST.get('company_name') and profile.is_employer:
            profile.company_name = request.POST.get('company_name')
        
        # Handle resume upload for job seekers
        if 'resume' in request.FILES and not profile.is_employer:
            profile.resume = request.FILES['resume']
            
        profile.save()
        messages.success(request, 'Profile updated successfully!')
        return redirect('job_list')
        
    return render(request, 'accounts/update_profile.html', {
        'user': user,
        'profile': profile
    })

@login_required
def view_profile(request):
    user = request.user
    profile = user.userprofile
    
    # Convert None values to empty strings to avoid "Not provided" display
    context = {
        'user': user,
        'profile': profile,
        'phone_number': profile.phone_number or '',
        'address': profile.address or '',
        'company_name': profile.company_name or '' if profile.is_employer else None
    }
    return render(request, 'accounts/view_profile.html', context)