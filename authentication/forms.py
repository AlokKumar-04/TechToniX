from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser  # Import your CustomUser model

class RegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    first_name = forms.CharField(max_length=30, required=False)
    last_name = forms.CharField(max_length=30, required=False)
    role = forms.ChoiceField(choices=[('attendee', 'Event Attendee')], required=True)

    class Meta(UserCreationForm.Meta):
        model = CustomUser  
        fields = UserCreationForm.Meta.fields + ('email', 'first_name', 'last_name', 'role')

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.role = self.cleaned_data['role']  
        if commit:
            user.save()
        return user

class SignInForm(forms.Form):
    username = forms.CharField(max_length=150)
    password = forms.CharField(widget=forms.PasswordInput)


''' class AttendeeProfileForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['first_name', 'last_name', 'email', 'bio', 'profile_picture']
        widgets = {
            'email': forms.EmailInput(attrs={'readonly': 'readonly'}),
            'bio': forms.Textarea(attrs={'rows': 3}),
        }
'''