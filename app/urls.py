from django.urls import path
from . import views

app_name = 'app'

urlpatterns = [
    path('', views.home, name='home'),
    path('dashboard/', views.attendee_dashboard, name='attendee_dashboard'),
    path('registrations/', views.view_registrations, name='view_registrations'),
    path('upcoming_events/', views.upcoming_events, name='upcoming_events'),
    path('profile/', views.user_profile_page, name='user_profile'),
    path('api/registrations/', views.AttendeeRegistrationListView.as_view(), name='api_attendee_registrations'),
    path('events/<int:event_id>/', views.event_detail, name='event_detail'),
    path('registrations/cancel/<int:registration_id>/', views.cancel_registration, name='cancel_registration'),
    path('api/events/<int:id>/', views.EventDetailView.as_view(), name='api_event_detail'),
    path('api/registrations/<int:id>/cancel/', views.RegistrationCancelView.as_view(), name='api_cancel_registration'),
    path('api/notifications/', views.NotificationListView.as_view(), name='api_notifications'),
    path('api/notifications/<int:id>/read/', views.NotificationReadView.as_view(), name='api_read_notification'),
]