from django.urls import path
from . import views

app_name = 'authentication'

urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', views.signin, name='SignIn'),
    path('logout/', views.logout_view, name='logout'),
    path('profile/', views.user_profile_page, name='profile')
    
]