from django.db import models

class EventAnalytics(models.Model):
    event = models.OneToOneField('event.Event', on_delete=models.CASCADE, related_name="analytics")
    total_registrations = models.PositiveIntegerField(default=0)
    total_views = models.PositiveIntegerField(default=0)
    total_check_ins = models.PositiveIntegerField(default=0)
    engagement_score = models.FloatField(default=0.0)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Analytics for {self.event.name}"