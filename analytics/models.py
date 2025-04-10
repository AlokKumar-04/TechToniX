from django.db import models

class EventAnalytics(models.Model):
    event = models.OneToOneField('event.Event', on_delete=models.CASCADE, related_name="analytics")
    total_registrations = models.PositiveIntegerField(default=0)
    daily_registrations = models.JSONField(default=dict, blank=True) # {'YYYY-MM-DD': count}
    weekly_registrations = models.JSONField(default=dict, blank=True) # {'YYYY-WW': count}
    total_views = models.PositiveIntegerField(default=0) # Keeping this as it's a useful metric
    total_check_ins = models.PositiveIntegerField(default=0) # Keeping this as it's a useful metric
    engagement_score = models.FloatField(default=0.0) # Keeping this for potential future use
    total_cancellations = models.PositiveIntegerField(default=0)
    cancellation_rate = models.FloatField(default=0.0)
    # Demographic Data (if available)
    age_group_distribution = models.JSONField(default=dict, blank=True) # {'18-25': count, '26-35': count, ...}
    location_distribution = models.JSONField(default=dict, blank=True) # {'City A': count, 'City B': count, ...}
    # Waitlist Statistics (if implemented)
    waitlist_size = models.PositiveIntegerField(default=0)
    waitlist_conversions = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Analytics for {self.event.name}"