from django.urls import path
from . import views

app_name = 'event'

urlpatterns = [
    path('', views.EventListView.as_view(), name='event_list'),
    path('category/<int:category_id>/', views.EventCategoryListView.as_view(), name='event_category_list'),
    path('<int:event_id>/', views.EventDetailView.as_view(), name='event_detail'),
    path('create/', views.EventCreateView.as_view(), name='event_create'),
    path('dashboard/', views.OrganizerDashboardView.as_view(), name='organizer_dashboard'),
    path('edit/<int:event_id>/', views.EventEditView.as_view(), name='event_edit'),
    path('delete/<int:event_id>/', views.EventDeleteView.as_view(), name='event_delete'),
    # ... other paths ...
    
]