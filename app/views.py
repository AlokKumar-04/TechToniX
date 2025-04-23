from django.utils import timezone
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from event.models import Event, Registration
from app.models import Notification
from django.template.defaulttags import register
from django.contrib import messages

def home(request):
    """
    View function to display the home page with upcoming events.
    """
    upcoming_events = Event.objects.filter(start_date__gte=timezone.now()).order_by('start_date')[:6]
    context = {
        'events': upcoming_events,
    }
    return render(request, 'app/home.html', context)


@register.filter
def chunks(lst, chunk_size):
    """
    Template filter to split a list into chunks.
    """
    for i in range(0, len(lst), chunk_size):
        yield lst[i:i + chunk_size]

@login_required
def attendee_dashboard(request):
    """
    View function for the attendee dashboard.
    """
    # Get the user's upcoming events
    upcoming_events = Event.objects.filter(registrations__user=request.user, start_date__gte=timezone.now()).distinct().order_by('start_date')
    # Get the user's registrations
    registrations = Registration.objects.filter(user=request.user).select_related('event').order_by('registration_date')
    #get notifications
    notifications = Notification.objects.filter(user=request.user).order_by('-timestamp')[:5]

    context = {
        'upcoming_events': upcoming_events,
        'registrations': registrations,
        'notifications':notifications,
    }
    return render(request, 'app/attendee_dashboard.html', context)

@login_required
def view_registrations(request):
    """
    View function to display the user's event registrations.
    """
    registrations = Registration.objects.filter(user=request.user).select_related('event').order_by('registration_date')
    return render(request, 'app/view_registrations.html', {'registrations': registrations})

@login_required
def upcoming_events(request):
    """
    View function to display events the user is registered for
    """
    events = Event.objects.filter(registrations__user=request.user, start_date__gte=timezone.now()).distinct().order_by('start_date')
    return render(request, 'app/upcoming_events.html', {'events': events})

@login_required
def event_detail(request, event_id):
    """
    View function to display details for a specific event.
    """
    event = get_object_or_404(Event, id=event_id)
    context = {
        'event': event,
    }
    return render(request, 'app/event_detail.html', context)

@login_required
def cancel_registration(request, registration_id):
    """
    View function to cancel a user's event registration.
    """
    registration = get_object_or_404(Registration, id=registration_id, user=request.user)
    if request.method == 'POST':
        registration.status = 'cancelled'
        registration.save()
        messages.success(request, "Registration cancelled successfully.")
        return redirect('app:view_registrations')
    context = {
        'registration': registration,
    }
    return render(request, 'app/cancel_registration.html', context)

@login_required
def view_notifications(request):
    """
    View function to display the user's notifications.
    """
    notifications = Notification.objects.filter(user=request.user).order_by('-timestamp')
    return render(request, 'app/view_notifications.html', {'notifications': notifications})

@login_required
def mark_notification_as_read(request, notification_id):
    """
    View function to mark a notification as read.
    """
    notification = get_object_or_404(Notification, id=notification_id, user=request.user)
    if request.method == 'POST':
        notification.is_read = True
        notification.save()
        return redirect('app:view_notifications')
    # Optionally, handle GET request if you want a confirmation page
    return render(request, 'app/mark_notification_read.html', {'notification': notification})

