from django.db import models
# from django.contrib.auth import get_user_model # Import get_user_model
# User = get_user_model() # Use get_user_model()

class PlatformAnalytics(models.Model):
    total_users = models.PositiveIntegerField(default=0)
    total_events = models.PositiveIntegerField(default=0)
    total_registrations = models.PositiveIntegerField(default=0)
    # Add other relevant platform-wide metrics here
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return "Platform Analytics"

class AdminActivityLog(models.Model):
    # user = models.ForeignKey(User, on_delete=models.CASCADE) # Use the User model
    timestamp = models.DateTimeField(auto_now_add=True)
    action = models.CharField(max_length=255)
    description = models.TextField()

    def __str__(self):
        return f"{self.timestamp} - {self.action}"
    
class EventApproval(models.Model):
    """
    Model to track event approval status.
    """
    event = models.OneToOneField('event.Event', on_delete=models.CASCADE, related_name='approval')
    is_approved = models.BooleanField(default=False)
    approved_by = models.ForeignKey('authentication.CustomUser', on_delete=models.SET_NULL, null=True, blank=True) #Should be CustomUser
    approved_at = models.DateTimeField(null=True, blank=True)
    
    def __str__(self):
        return f"Approval status for {self.event.name}: {self.is_approved}"
