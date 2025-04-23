from django.urls import path
from . import views

app_name = 'event'

urlpatterns = [
    # Event URLs (existing ones)
    path('register/<int:event_id>/', views.register_for_event, name='register_for_event'),
    path('my-registrations/', views.user_event_registrations, name='user_event_registrations'),
    path('cancel-registration/<int:registration_id>/', views.cancel_event_registration, name='cancel_event_registration'),
    path('<int:event_id>/', views.event_detail, name='event_detail'),  # Add this line
    # Ticket URLs
    path('<int:event_id>/tickets/create/', views.create_ticket, name='create_ticket'),
    path('<int:event_id>/tickets/', views.list_tickets, name='list_tickets'),
    path('tickets/<int:ticket_id>/update/', views.update_ticket, name='update_ticket'),
    path('tickets/<int:ticket_id>/delete/', views.delete_ticket, name='delete_ticket'),
]
