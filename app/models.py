from django.db import models
from django.conf import settings # Import settings
from event.models import Event

class Notification(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE) # Correctly reference the user model
    message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)
    notification_type = models.CharField(max_length=50)
    related_event = models.ForeignKey(Event, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.message