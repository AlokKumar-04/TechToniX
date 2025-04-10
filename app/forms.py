from django import forms
from event.models import Event

class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = '__all__'  # Or specify the fields you want in the form
        # You can also customize widgets, labels, help_text here if needed
        widgets = {
            'date': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'end_date': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }