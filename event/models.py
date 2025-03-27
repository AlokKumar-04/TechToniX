from django.db import models
from django.conf import settings  # Import settings

class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    icon_class = models.CharField(max_length=50, help_text="CSS class for icons (e.g., 'bx bx-laptop')", null=True, blank=True)

    def __str__(self):
        return self.name


class Event(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending Approval'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    ]

    name = models.CharField(max_length=255)
    description = models.TextField()
    date = models.DateTimeField()
    location = models.CharField(max_length=255)
    organizer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='organized_events')
    category = models.ForeignKey('event.Category', on_delete=models.SET_NULL, null=True, blank=True)  # Added category
    event_image = models.ImageField(upload_to='event_images/', blank=True, null=True)  # Added event image
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.get_status_display()}"


class Ticket(models.Model):
    event = models.ForeignKey('event.Event', on_delete=models.CASCADE, related_name='tickets')
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity_available = models.PositiveIntegerField(default=0)
    # Potentially add fields for sale start/end dates, etc.

    def __str__(self):
        return f"{self.name} - {self.event.name}"


class Registration(models.Model):
    # Use settings.AUTH_USER_MODEL
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='registrations')
    event = models.ForeignKey('event.Event', on_delete=models.CASCADE, related_name='registrations')
    ticket = models.ForeignKey('event.Ticket', on_delete=models.SET_NULL, null=True, blank=True) # Link to the specific ticket purchased
    registration_date = models.DateTimeField(auto_now_add=True)
    is_approved = models.BooleanField(default=True) # No more 'pending' status for registration itself
    is_checked_in = models.BooleanField(default=False)

    class Meta:
        unique_together = ('user', 'event', 'ticket') # Ensure a user can't register for the same ticket type for the same event multiple times

    def __str__(self):
        return f"{self.user} registered for {self.event.name} ({self.ticket.name if self.ticket else 'General Admission'})"


class EventAnalytics(models.Model):
    event = models.OneToOneField('event.Event', on_delete=models.CASCADE, related_name="analytics")
    total_registrations = models.PositiveIntegerField(default=0)
    total_views = models.PositiveIntegerField(default=0)
    total_check_ins = models.PositiveIntegerField(default=0)  # New: Track attendees who actually checked in
    engagement_score = models.FloatField(default=0.0)  # New: AI-based or manually calculated

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Analytics for {self.event.name}"