from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib import messages
from django.utils import timezone
from authentication.models import CustomUser  # Changed User to CustomUser
from event.models import Event, Category


# Helper function to check if a user is an admin
def is_admin(user):
    return user.is_staff


# Admin Views
@user_passes_test(is_admin)
def admin_home_view(request):
    """
    View for the admin homepage.
    """
    # Add logic to fetch data for the admin homepage if needed
    return render(request, 'management/home.html')


@user_passes_test(is_admin)
def admin_dashboard_view(request):
    """
    View for the admin dashboard.  Displays key metrics.
    """
    total_events = Event.objects.count()
    approved_events = Event.objects.filter(status='published').count()  # Adjust status as needed
    pending_events = Event.objects.filter(status='draft').count()    # Adjust status as needed
    rejected_events = Event.objects.filter(status='inactive').count()  # Adjust status as needed
    total_users = CustomUser.objects.count()  # Use your CustomUser model here
    # Example: Calculate new users in the last 30 days (adjust as needed)
    thirty_days_ago = timezone.now() - timezone.timedelta(days=30)
    new_users_30_days = CustomUser.objects.filter(date_joined__gte=thirty_days_ago).count()  # Use CustomUser

    context = {
        'total_events': total_events,
        'approved_events': approved_events,
        'pending_events': pending_events,
        'rejected_events': rejected_events,
        'total_users': total_users,
        'new_users_30_days': new_users_30_days,
    }
    return render(request, 'management/dashboard.html', context)


@user_passes_test(is_admin)
def admin_profile_view(request):
    """
    View for the admin's profile page.
    """
    return render(request, 'management/profile.html')


@user_passes_test(is_admin)
def admin_profile_update_view(request):
    """
    View to update the admin's profile information.
    """
    if request.method == 'POST':
        user = request.user
        user.email = request.POST.get('email', user.email)
        user.first_name = request.POST.get('first_name', user.first_name)
        user.last_name = request.POST.get('last_name', user.last_name)
        user.save()
        messages.success(request, 'Profile updated successfully!')
        return redirect('management:admin_profile')  # Use management namespace
    return redirect('management:admin_profile')  # Redirect if not POST


@user_passes_test(is_admin)
def admin_password_change_view(request):
    """
    View to change the admin's password.
    """
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request, 'Password changed successfully!')
            return redirect('management:admin_profile')  # Use management namespace
        else:
            return render(request, 'management/profile.html', {'password_change_errors': form.errors})
    return redirect('management:admin_profile')  # Redirect if not POST


@user_passes_test(is_admin)
def admin_event_management_view(request):
    """
    View to display and manage events.
    """
    events = Event.objects.all()
    return render(request, 'management/event_management.html', {'events': events})


@user_passes_test(is_admin)
def admin_event_create_view(request):
    """
    View to create a new event.
    """
    if request.method == 'POST':
        name = request.POST.get('name')
        description = request.POST.get('description')
        start_date_str = request.POST.get('start_date')  # Changed from date to start_date
        end_date_str = request.POST.get('end_date')
        location = request.POST.get('location')
        category_name = request.POST.get('category')
        event_image = request.FILES.get('event_image')
        status = request.POST.get('status', 'draft')  # Default to draft if not provided

        # Basic validation
        errors = {}
        if not name:
            errors['name'] = 'Name is required'
        if not start_date_str:  # changed from date
            errors['start_date'] = 'Start Date is required'
        if not end_date_str:
            errors['end_date'] = 'End Date is required'
        if not location:
            errors['location'] = 'Location is required'

        if errors:
            messages.error(request, 'Please fix the errors below')
            return render(request, 'management/event_create.html', {'errors': errors})

        try:
            start_date = timezone.datetime.fromisoformat(start_date_str.replace('T', ' '))  # Adjust format if needed
            end_date = timezone.datetime.fromisoformat(end_date_str.replace('T', ' '))
        except ValueError:
            messages.error(request, 'Invalid date and time format.')
            return render(request, 'management/event_create.html')

        if end_date < start_date:
            messages.error(request, 'End date cannot be earlier than start date')
            return render(request, 'management/event_create.html')

        try:
            category = Category.objects.get(name=category_name)
        except Category.DoesNotExist:
            category = None  # Or handle the error as needed

        event = Event(
            name=name,
            description=description,
            start_date=start_date,  # changed from date to start_date
            end_date=end_date,
            location=location,
            organizer=request.user,  # Assuming the logged-in admin is the organizer
            category=category,
            event_image=event_image,
            status=status
        )
        event.save()
        messages.success(request, f'Event "{event.name}" created successfully!')
        return redirect('management:event_management')
    else:
        return render(request, 'management/event_create.html')


@user_passes_test(is_admin)
def admin_event_update_view(request, event_id):
    """
    View to update an existing event.
    """
    event = get_object_or_404(Event, id=event_id)
    if request.method == 'POST':
        name = request.POST.get('name')
        description = request.POST.get('description')
        start_date_str = request.POST.get('start_date')  # changed
        end_date_str = request.POST.get('end_date')
        location = request.POST.get('location')
        category_name = request.POST.get('category')
        event_image = request.FILES.get('event_image')
        status = request.POST.get('status')

        # Basic validation
        errors = {}
        if not name:
            errors['name'] = 'Name is required'
        if not start_date_str:  # changed
            errors['start_date'] = 'Start Date is required'
        if not end_date_str:
            errors['end_date'] = 'End Date is required'
        if not location:
            errors['location'] = 'Location is required'

        if errors:
            messages.error(request, 'Please fix the errors below')
            return render(request, 'management/event_update.html', {'event': event, 'errors': errors})

        try:
            start_date = timezone.datetime.fromisoformat(start_date_str.replace('T', ' '))  # Adjust format if needed
            end_date = timezone.datetime.fromisoformat(end_date_str.replace('T', ' '))
        except ValueError:
            messages.error(request, 'Invalid date and time format.')
            return render(request, 'management/event_update.html', {'event': event})

        if end_date < start_date:
            messages.error(request, 'End date cannot be earlier than start date')
            return render(request, 'management/event_update.html', {'event': event})

        try:
            category = Category.objects.get(name=category_name)
        except Category.DoesNotExist:
            category = None  # Or handle the error as needed

        event.name = name
        event.description = description
        event.start_date = start_date  # changed
        event.end_date = end_date
        event.location = location
        event.category = category
        if event_image:
            event.event_image = event_image
        event.status = status
        event.save()
        messages.success(request, f'Event "{event.name}" updated successfully!')
        return redirect('management:event_management')
    else:
        return render(request, 'management/event_update.html', {'form': {}, 'event': event})  # Pass an empty form context


@user_passes_test(is_admin)
def admin_event_delete_view(request, event_id):
    """
    View to delete an event.  Uses POST for the delete operation.
    """
    event = get_object_or_404(Event, id=event_id)
    if request.method == 'POST':  # It's better to use POST for delete
        event.delete()
        messages.success(request, f'Event "{event.name}" deleted successfully!')
        return redirect('management:admin_event_management')
    else:
        # For security, you might want to display a confirmation page here instead of just deleting on GET
        return render(request, 'management/event_confirm_delete.html', {'event': event})  # Create this template


@user_passes_test(is_admin)
def admin_ticket_requests_view(request):
    # Add logic to fetch and display ticket requests
    return render(request, 'management/ticket_requests.html')  # Create this template later


@user_passes_test(is_admin)
def admin_analytics_view(request):
    # Add logic to fetch and display admin analytics
    return render(request, 'management/analytics.html')  # Create this template later


@user_passes_test(is_admin)
def admin_user_management_view(request):
    """
    View to manage users.
    """
    users = CustomUser.objects.all()  # changed
    return render(request, 'management/user_management.html', {'users': users})  # create this template later
