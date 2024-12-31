from django.urls import path
from . import views

urlpatterns = [
    path('process/<int:job_id>/', views.payment_process, name='payment_process'),
    path('history/', views.payment_history, name='payment_history'),
] 