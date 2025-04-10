from django.urls import path
from . import views

app_name = 'authentication'

urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', views.signin, name='SignIn'),
    path('logout/', views.logout_view, name='logout'),
    path('api/profile/', views.UserProfileView.as_view(), name='api_user_profile'),
    
]