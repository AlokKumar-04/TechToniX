from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

app_name = 'authentication'

urlpatterns = [
    path('register/', views.RegisterView.as_view(), name='register'),
    path('login/', views.SignInView.as_view(), name='SignIn'),
    path('logout/', auth_views.LogoutView.as_view(next_page='app:home'), name='logout'),
    path('profile/', views.ProfileView.as_view(), name='Profile'),
    path('profile/edit/', views.EditProfileView.as_view(), name='edit_profile'),

    path('password_reset/', auth_views.PasswordResetView.as_view(
        template_name='authentication/password_reset_form.html',
        email_template_name='authentication/password_reset_email.html',
        success_url='done/'
    ), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(
        template_name='authentication/password_reset_done.html'
    ), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(
        template_name='authentication/password_reset_confirm.html',
        success_url='/reset/done/'
    ), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(
        template_name='authentication/password_reset_complete.html'
    ), name='password_reset_complete'),
]