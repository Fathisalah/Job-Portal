from django.urls import path
from . import views

urlpatterns = [
    path('', views.job_list, name='job_list'),
    path('post/', views.post_job, name='post_job'),
    path('job/<int:job_id>/', views.job_detail, name='job_detail'),
    path('job/<int:job_id>/apply/', views.apply_job, name='apply_job'),
    path('employer/dashboard/', views.employer_dashboard, name='employer_dashboard'),
    path('application/<int:application_id>/update/', views.update_application_status, name='update_application_status'),
] 