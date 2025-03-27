from django.shortcuts import render
from event.models import Event  

def home(request):
    
    upcoming_events = Event.objects.filter(status='approved').order_by('date')[:6] 

    return render(request, 'app/home.html', {'events': upcoming_events})