from rest_framework.generics import RetrieveUpdateAPIView
from rest_framework.permissions import IsAuthenticated
from .serializers import UserProfileSerializer
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from .forms import SignInForm, RegistrationForm



class UserProfileView(RetrieveUpdateAPIView):
    serializer_class = UserProfileSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user
    
    

def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request, 'Account created successfully!')
            return redirect('authentication:SignIn')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{field.capitalize()}: {error}")
    else:
        form = RegistrationForm()
    return render(request, 'authentication/register.html', {'form': form})



def signin(request):
    if request.method == 'POST':
        form = SignInForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f'Logged in as {username}.')
                if user.is_staff:
                    return redirect('management:admin_dashboard')  # Redirect admin users to the admin dashboard
                else:
                    return redirect('app:home')  # Redirect regular users to the homepage
            else:
                messages.error(request, 'Invalid username or password.')
        else:
            for error in form.errors.values():
                messages.error(request, error.as_text())
    else:
        form = SignInForm()
    return render(request, 'authentication/signin.html', {'form': form})


@login_required
def logout_view(request):
    logout(request)
    messages.info(request, 'Logged out successfully.')
    return redirect('app:home')  