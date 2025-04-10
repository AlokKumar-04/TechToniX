from rest_framework import serializers
from event.models import Registration, Event
from app.models import Notification

class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = ['id', 'name', 'event_image', 'date', 'location', 'description', 'organizer'] # Include all necessary fields

class RegistrationSerializer(serializers.ModelSerializer):
    event = EventSerializer(read_only=True) # Use the EventSerializer

    class Meta:
        model = Registration
        fields = ['id', 'event', 'registration_date', 'status']

class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = ['id', 'message', 'timestamp', 'is_read', 'notification_type', 'related_event']