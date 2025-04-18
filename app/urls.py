from django.urls import path
from . import views

app_name = 'app'

urlpatterns = [
    path('', views.home, name='home'),
    path('dashboard/', views.attendee_dashboard, name='attendee_dashboard'),
    path('registrations/', views.view_registrations, name='view_registrations'),
    path('upcoming_events/', views.upcoming_events, name='upcoming_events'),
    path('event/<int:event_id>/', views.event_detail, name='event_detail'),
    path('cancel_registration/<int:registration_id>/', views.cancel_registration, name='cancel_registration'),
    path('notifications/', views.view_notifications, name='view_notifications'),
    path('notifications/read/<int:notification_id>/', views.mark_notification_as_read, name='mark_notification_as_read'),
    
]