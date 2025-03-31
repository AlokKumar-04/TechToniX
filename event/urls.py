from django.urls import path
from . import views

app_name = 'event'

urlpatterns = [
    path('', views.event_list, name='event_list'),
    path('create/', views.event_create, name='event_create'),
    path('dashboard/', views.organizer_dashboard, name='organizer_dashboard'),
    path('<int:event_id>/', views.event_detail, name='event_detail'),
    path('<int:event_id>/register/<int:ticket_id>/', views.register_for_event, name='register_for_event'),
    path('registrations/', views.user_registrations, name='user_registrations'),
    path('registrations/cancel/<int:registration_id>/', views.cancel_registration, name='cancel_registration'),
    path('edit/<int:event_id>/', views.event_edit, name='event_edit'),
    path('delete/<int:event_id>/', views.event_delete, name='event_delete'),
]