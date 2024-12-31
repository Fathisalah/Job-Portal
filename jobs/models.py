from django.db import models
from accounts.models import UserProfile

class Job(models.Model):
    employer = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    description = models.TextField()
    requirements = models.TextField()
    location = models.CharField(max_length=100)
    salary = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    application_fee = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-created_at']

class JobApplication(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending Review'),
        ('shortlisted', 'Shortlisted'),
        ('interviewing', 'Interviewing'),
        ('selected', 'Selected'),
        ('rejected', 'Rejected')
    ]
    
    job = models.ForeignKey(Job, on_delete=models.CASCADE)
    applicant = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    applied_at = models.DateTimeField(auto_now_add=True)
    cover_letter = models.TextField()

    class Meta:
        unique_together = ['job', 'applicant']
        ordering = ['-applied_at']

    def __str__(self):
        return f"{self.applicant.user.username} - {self.job.title}"

    def get_status_badge_color(self):
        return {
            'pending': 'warning',
            'shortlisted': 'info',
            'interviewing': 'primary',
            'selected': 'success',
            'rejected': 'danger'
        }.get(self.status, 'secondary') 