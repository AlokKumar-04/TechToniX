from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from django.db import IntegrityError
import re


User = get_user_model()


@login_required
def user_profile_page(request):
    """
    View function for displaying and updating the user's profile page.

    Handles both GET requests (displaying the profile) and POST requests
    (updating the profile).
    """
    User = get_user_model() # Get the user model
    if request.method == 'POST':
        # Process the form submission to update user data
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        bio = request.POST.get('bio')
        profile_picture = request.FILES.get('profile_picture')  # Get the uploaded file

        errors = {}  # Dictionary to store validation errors

        # Basic validation: Check for required fields
        if not first_name:
            errors['first_name'] = 'First name is required.'
        if not last_name:
            errors['last_name'] = 'Last name is required.'

        if errors:
            # If there are errors, re-render the form with the error messages
            return render(request, 'authentication/profile.html', {'errors': errors})
        else:
            try:
                # Update the user's attributes
                user = request.user
                user.first_name = first_name
                user.last_name = last_name
                user.bio = bio
                if profile_picture:
                    user.profile_picture = profile_picture  # Assign the uploaded file

                user.save()  # Save the changes to the database
                messages.success(request, 'Profile updated successfully!')
                return redirect('authentication:profile')  # Redirect to the profile page
            except Exception as e:
                # Handle any exceptions that occur during the update process
                messages.error(request, f'There was an error updating your profile: {e}')
                return render(request, 'authentication/profile.html', {'errors': {'non_field_errors': [f'Error: {e}']}})
    else:
        # For a GET request, render the profile page with the user's data
        # Pass the user object to the template context
        user = request.user
        return render(request, 'app/profile.html', {'user': user})




def register(request):
    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        email = request.POST.get('email', '').strip().lower()
        password = request.POST.get('password', '')
        password2 = request.POST.get('password2', '')
        agree_terms = request.POST.get('agree_terms')

        errors = {}

        # Username validation
        if not username:
            errors['username'] = 'Username is required.'
        elif len(username) < 4:
            errors['username'] = 'Username must be at least 4 characters.'
        elif not re.match(r'^[\w.@+-]+\Z', username):
            errors['username'] = 'Enter a valid username. Letters, digits and @/./+/-/_ only.'

        # Email validation
        if not email:
            errors['email'] = 'Email is required.'
        else:
            try:
                validate_email(email)
            except ValidationError:
                errors['email'] = 'Enter a valid email address.'

        # Password validation
        if not password:
            errors['password'] = 'Password is required.'
        else:
            if len(password) < 8:
                errors['password'] = 'Password must be at least 8 characters.'
            if not re.search(r'[A-Z]', password):
                errors['password'] = 'Password must contain at least one uppercase letter.'
            if not re.search(r'[a-z]', password):
                errors['password'] = 'Password must contain at least one lowercase letter.'
            if not re.search(r'[0-9]', password):
                errors['password'] = 'Password must contain at least one number.'
            if not re.search(r'[^A-Za-z0-9]', password):
                errors['password'] = 'Password must contain at least one special character.'

        # Password confirmation
        if password != password2:
            errors['password2'] = 'Passwords do not match.'

        # Terms agreement
        if not agree_terms:
            errors['terms'] = 'You must agree to the terms and conditions.'

        if errors:
            return render(request, 'authentication/register.html', {
                'errors': errors,
                'username': username,
                'email': email
            })

        try:
            user = User.objects.create_user(
                username=username,
                email=email,
                password=password
            )
            messages.success(request, '🎉 Account created successfully! You can now sign in.')
            return redirect('authentication:SignIn')
            
        except IntegrityError as e:
            if 'username' in str(e).lower():
                errors['username'] = 'Username is already taken.'
            elif 'email' in str(e).lower():
                errors['email'] = 'Email is already registered.'
            else:
                messages.error(request, '⚠️ Error creating account. Please try again.')
            
            return render(request, 'authentication/register.html', {
                'errors': errors,
                'username': username,
                'email': email
            })
            
        except Exception as e:
            messages.error(request, f'⚠️ Unexpected error: {str(e)}')
            return render(request, 'authentication/register.html', {
                'username': username,
                'email': email
            })

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