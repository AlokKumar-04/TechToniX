from django.utils import timezone
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from event.models import Event, Registration
from app.models import Notification
from django.template.defaulttags import register

def home(request):
    upcoming_events = Event.objects.filter(date__gte=timezone.now()).order_by('date')[:6]
    context = {
        'events': upcoming_events,
    }
    return render(request, 'app/home.html', context)


@register.filter
def chunks(lst, chunk_size):
    for i in range(0, len(lst), chunk_size):
        yield lst[i:i + chunk_size]

@login_required
def attendee_dashboard(request):
    return render(request, 'app/attendee_dashboard.html')

@login_required
def view_registrations(request):
    registrations = Registration.objects.filter(user=request.user).select_related('event')
    return render(request, 'app/view_registrations.html', {'registrations': registrations})

@login_required
def upcoming_events(request):
    events = Event.objects.filter(registrations__user=request.user).distinct()
    return render(request, 'app/upcoming_events.html', {'events': events})

@login_required
def event_detail(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    context = {
        'event': event,
    }
    return render(request, 'app/event_detail.html', context)

@login_required
def cancel_registration(request, registration_id):
    registration = get_object_or_404(Registration, id=registration_id, user=request.user)
    if request.method == 'POST':
        registration.status = 'cancelled'
        registration.save()
        return redirect('app:attendee_dashboard') # Redirect back to the dashboard
    context = {
        'registration': registration,
    }
    return render(request, 'app/cancel_registration.html', context)

@login_required
def view_notifications(request):
    notifications = Notification.objects.filter(user=request.user).order_by('-timestamp')
    return render(request, 'app/view_notifications.html', {'notifications': notifications})

@login_required
def mark_notification_as_read(request, notification_id):
    notification = get_object_or_404(Notification, id=notification_id, user=request.user)
    if request.method == 'POST':
        notification.is_read = True
        notification.save()
        return redirect('app:view_notifications') # Redirect back to notifications
    # Optionally, handle GET request if you want a confirmation page
    return render(request, 'app/mark_notification_read.html', {'notification': notification})
