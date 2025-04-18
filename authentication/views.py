from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages



@login_required
def user_profile_page(request):
    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        bio = request.POST.get('bio')
        profile_picture = request.FILES.get('profile_picture')

        errors = {}
        if not first_name:
            errors['first_name'] = 'First name is required.'
        if not last_name:
            errors['last_name'] = 'Last name is required.'

        if errors:
            return render(request, 'authentication/profile.html', {'errors': errors})
        else:
            try:
                request.user.first_name = first_name
                request.user.last_name = last_name
                request.user.bio = bio
                if profile_picture:
                    request.user.profile_picture = profile_picture
                request.user.save()
                messages.success(request, 'Profile updated successfully!')
                return redirect('authentication:profile')
            except Exception as e:
                messages.error(request, f'There was an error updating your profile: {e}')
                return render(request, 'authentication/profile.html', {'errors': {'non_field_errors': [f'Error: {e}']}})
    else:
        return render(request, 'app/profile.html')


def register(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        password2 = request.POST.get('password2')

        errors = {}

        if not username:
            errors['username'] = 'Username is required.'
        if not email:
            errors['email'] = 'Email is required.'
        else:
            try:
                from django.core.validators import validate_email
                from django.core.exceptions import ValidationError
                validate_email(email)
            except ValidationError:
                errors['email'] = 'Enter a valid email address.'
        if not password:
            errors['password'] = 'Password is required.'
        elif len(password) < 6:
            errors['password'] = 'Password must be at least 6 characters long.'
        if password != password2:
            errors['password2'] = 'Passwords do not match.'

        if errors:
            return render(request, 'authentication/register.html', {'errors': errors, 'username': username, 'email': email})
        else:
            try:
                user = User.objects.create_user(username=username, email=email, password=password)
                messages.success(request, 'Account created successfully! You can now sign in.')
                return redirect('authentication:SignIn')
            except IntegrityError as e:
                if 'unique constraint' in str(e).lower() and 'username' in str(e).lower():
                    errors['username'] = 'That username is already taken.'
                elif 'unique constraint' in str(e).lower() and 'email' in str(e).lower():
                    errors['email'] = 'That email address is already registered.'
                else:
                    messages.error(request, f'Error creating account: {e}')
                return render(request, 'authentication/register.html', {'errors': errors, 'username': username, 'email': email})
            except Exception as e:
                messages.error(request, f'An unexpected error occurred: {e}')
                return render(request, 'authentication/register.html', {'username': username, 'email': email})
    else:
        return render(request, 'authentication/register.html')



def signin(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        if not username:
            messages.error(request, 'Username is required.')
        elif not password:
            messages.error(request, 'Password is required.')
        else:
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f'Logged in as {username}.')
                if user.is_staff: # or user.is_admin
                    return redirect('management:admin_dashboard')
                else:
                    return redirect('app:home')
            else:
                messages.error(request, 'Invalid username or password.')
    return render(request, 'authentication/signin.html')


@login_required
def logout_view(request):
    logout(request)
    messages.info(request, 'Logged out successfully.')
    return redirect('app:home')