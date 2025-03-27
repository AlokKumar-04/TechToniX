from django import forms
from .models import Event, Ticket
from django.forms.models import inlineformset_factory

class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = ['name', 'description', 'date', 'location', 'category', 'event_image']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
            'date': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }

class TicketForm(forms.ModelForm):
    class Meta:
        model = Ticket
        fields = ['name', 'description', 'price', 'quantity_available']

TicketFormSet = inlineformset_factory(Event, Ticket, form=TicketForm, extra=1, can_delete=True)