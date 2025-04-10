from django.utils import timezone
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from event.models import Event, Registration
from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from app.models import Notification
from .serializers import RegistrationSerializer, EventSerializer, NotificationSerializer

def home(request):
    upcoming_events = Event.objects.filter(date__gte=timezone.now()).order_by('date')[:6]
    context = {
        'events': upcoming_events,
    }
    return render(request, 'app/home.html', context)

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
def user_profile_page(request):
    return render(request, 'app/profile.html')

class AttendeeRegistrationListView(generics.ListAPIView):
    serializer_class = RegistrationSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return Registration.objects.filter(user=user).select_related('event').order_by('-registration_date')

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

class EventDetailView(generics.RetrieveAPIView):
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    permission_classes = [AllowAny] # Or IsAuthenticated if needed
    lookup_field = 'id'

class RegistrationCancelView(generics.UpdateAPIView):
    queryset = Registration.objects.all()
    serializer_class = RegistrationSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = 'id'

    def update(self, request, *args, **kwargs):
        instance = self.get_object()

        # Check if the registration belongs to the logged-in user
        if instance.user != request.user:
            return Response({'detail': 'You do not have permission to cancel this registration.'}, status=status.HTTP_403_FORBIDDEN)

        # Update the registration status
        instance.status = 'cancelled'
        instance.save()

        serializer = self.get_serializer(instance)
        return Response(serializer.data)


class NotificationListView(generics.ListAPIView):
    serializer_class = NotificationSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Notification.objects.filter(user=self.request.user).order_by('-timestamp')

class NotificationReadView(generics.UpdateAPIView):
    queryset = Notification.objects.all()
    serializer_class = NotificationSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = 'id'

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.user != request.user:
            return Response({'detail': 'You do not have permission to mark this notification as read.'}, status=status.HTTP_403_FORBIDDEN)
        instance.is_read = True
        instance.save()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)