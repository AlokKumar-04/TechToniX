from django.shortcuts import render, redirect
from django.contrib.auth import get_user_model, login, authenticate
from django.contrib.auth import logout
from django.contrib import messages
from django.views import View
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from authentication.forms import UserProfileForm


User = get_user_model()

@method_decorator(login_required, name='dispatch')
class ProfileView(View):
    template_name = 'authentication/profile.html'

    def get(self, request):
        form = UserProfileForm(instance=request.user)
        return render(request, self.template_name, {'form': form})

@method_decorator(login_required, name='dispatch')
class EditProfileView(View):
    template_name = 'authentication/edit_profile.html'

    def get(self, request):
        form = UserProfileForm(instance=request.user)
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = UserProfileForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your profile has been updated successfully!')
            return redirect('authentication:Profile')
        else:
            messages.error(request, 'There was an error updating your profile. Please correct the fields below.')
            return render(request, self.template_name, {'form': form})

class RegisterView(View):
    template_name = 'authentication/register.html'

    def get(self, request):
        form_data = {
            'username': request.GET.get('username', ''),
            'email': request.GET.get('email', ''),
            'role': request.GET.get('role', 'attendee'),
        }
        return render(request, self.template_name, form_data)

    def post(self, request):
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        password2 = request.POST.get('password2')
        role = request.POST.get('role', 'attendee')
        terms = request.POST.get('terms')

        errors = {}

        # Basic server-side validation (redundant but good practice)
        if not username or len(username.strip()) < 4:
            errors['username'] = "Username must be at least 4 characters."
        if not email or '@' not in email or '.' not in email:
            errors['email'] = "Invalid email format."
        if not password or len(password) < 6 or not any(char.isdigit() for char in password) or not any(char in "!@#$%^&*()" for char in password):
            errors['password'] = "Password must be at least 6 characters long, include a number and a special character."
        if password != password2:
            errors['password2'] = "Passwords do not match."
        if not terms:
            errors['terms'] = "You must agree to the terms."

        if errors:
            for field, error in errors.items():
                messages.error(request, error)
            # Re-render the form with the submitted data
            return render(request, self.template_name, {
                'username': username,
                'email': email,
                'role': role,
            })

        try:
            user = User.objects.create_user(username=username, email=email, password=password)
            user.role = role  # Corrected line: directly set the role
            user.save()
            login(request, user)
            messages.success(request, f"Account created successfully! You are now logged in as {username}.")
            return redirect('home')  # Redirect to your home page
        except Exception as e:
            # Handle potential database errors (e.g., username already exists)
            messages.error(request, f"An error occurred during registration: {e}")
            return render(request, self.template_name, {
                'username': username,
                'email': email,
                'role': role,
            })
        


class SignInView(View):
    template_name = 'authentication/signin.html'

    def get(self, request):
        return render(request, self.template_name)

    def post(self, request):
        username = request.POST.get('username')
        password = request.POST.get('password')
        remember_me = request.POST.get('rememberMe')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            messages.success(request, f"Logged in successfully as {username}.")
            if not remember_me:
                request.session.set_expiry(0) # Session expires when browser closes
            return redirect('app:home')  
        else:
            messages.error(request, "Invalid username or password.")
            return render(request, self.template_name, {'username': username}) # Re-render with the entered username
        

@method_decorator(login_required, name='dispatch')
class CustomLogoutView(View):
    def get(self, request):
        logout(request)
        return redirect('app:home')