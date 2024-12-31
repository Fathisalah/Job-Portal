from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('register/', views.register, name='register'),
    path('logout/', views.logout_view, name='logout'),
    path('profile/update/', views.update_profile, name='update_profile'),
    path('profile/', views.view_profile, name='view_profile'),
] 