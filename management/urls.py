from django.urls import path
from . import views

app_name = 'management'

urlpatterns = [
    path('', views.admin_home_view, name='admin_home'),
    path('dashboard/', views.admin_dashboard_view, name='admin_dashboard'),
    path('profile/', views.admin_profile_view, name='admin_profile'),
    path('profile/update/', views.admin_profile_update_view, name='admin_profile_update'),
    path('profile/password/', views.admin_password_change_view, name='admin_password_change'),
    path('events/', views.admin_event_management_view, name='event_management'),
    path('events/create/', views.admin_event_create_view, name='admin_event_create'),
    path('events/update/<int:event_id>/', views.admin_event_update_view, name='admin_event_update'),
    path('events/delete/<int:event_id>/', views.admin_event_delete_view, name='admin_event_delete'),
    path('ticket-requests/', views.admin_ticket_requests_view, name='admin_ticket_requests'),
    path('analytics/', views.admin_analytics_view, name='admin_analytics'),
    path('users/', views.admin_user_management_view, name='admin_user_management'),
]