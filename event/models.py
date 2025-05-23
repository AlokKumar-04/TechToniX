from django.db import models
from django.conf import settings

class Category(models.Model):
    CATEGORY_CHOICES = [
        ('tech', 'Tech'),
        ('music', 'Music'),
        ('business', 'Business'),
    ]
    name = models.CharField(max_length=100, choices=CATEGORY_CHOICES)
    icon_class = models.CharField(max_length=50, help_text="CSS class for icons (e.g., 'bx bx-laptop')", null=True, blank=True)

    def __str__(self):
        return dict(self.CATEGORY_CHOICES).get(self.name, self.name)


class Event(models.Model):
    STATUS_CHOICES = [
        ('draft', 'Draft'),
        ('published', 'Published'),
        ('inactive', 'Inactive'),
        ('cancelled', 'Cancelled'),
        ('archived', 'Archived'),
    ]

    name = models.CharField(max_length=255)
    description = models.TextField()
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    location = models.CharField(max_length=255)
    organizer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='organized_events')
    category = models.ForeignKey('event.Category', on_delete=models.SET_NULL, null=True, blank=True)
    event_image = models.ImageField(upload_to='event_images/', blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='draft')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.get_status_display()}"


class Ticket(models.Model):
    STATUS_CHOICES = [
        ('available', 'Available'),
        ('sold_out', 'Sold Out'),
        ('on_hold', 'On Hold'),
        ('cancelled', 'Cancelled'),
    ]
    event = models.ForeignKey('event.Event', on_delete=models.CASCADE, related_name='tickets')
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity_available = models.PositiveIntegerField(default=0)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='available')
    # Potentially add fields for sale start/end dates, etc.

    def __str__(self):
        return f"{self.name} - {self.event.name} ({self.get_status_display()})"


class Registration(models.Model):
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('cancelled', 'Cancelled'),
        ('completed', 'Completed'),
        ('held', 'Held'),
    ]
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='registrations')
    event = models.ForeignKey('event.Event', on_delete=models.CASCADE, related_name='registrations')
    ticket = models.ForeignKey('event.Ticket', on_delete=models.SET_NULL, null=True, blank=True)
    registration_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='active')
    is_checked_in = models.BooleanField(default=False)

    class Meta:
        unique_together = ('user', 'event', 'ticket')

    def __str__(self):
        return f"{self.user} registered for {self.event.name} ({self.ticket.name if self.ticket else 'General Admission'}) - {self.get_status_display()}"