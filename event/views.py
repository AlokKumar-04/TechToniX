from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from .models import Event, Ticket, Registration  # Import your models
from django.contrib.auth.models import User
from management.views import is_admin # Import the is_admin function from management.views


@login_required
def register_for_event(request, event_id):
    """View to register a user for an event."""
    event = get_object_or_404(Event, pk=event_id)

    if request.method == 'POST':
        ticket_id = request.POST.get('ticket_id')
        try:
            ticket = Ticket.objects.get(pk=ticket_id, event=event)
        except Ticket.DoesNotExist:
            messages.error(request, "Invalid ticket type selected.")
            return redirect('event:event_detail', event_id=event_id)

        # Check if the user is already registered for this event with this ticket
        if Registration.objects.filter(user=request.user, event=event, ticket=ticket).exists():
            messages.warning(request, "You are already registered for this event with this ticket.")
            return redirect('event:user_event_registrations')

        # Create the registration
        registration = Registration.objects.create(user=request.user, event=event, ticket=ticket)
        messages.success(request, "Successfully registered for the event.")
        return redirect('event:user_event_registrations')

    return render(request, 'event/event_detail.html', {'event': event})  # Or wherever you want to redirect


@login_required
def user_event_registrations(request):
    """View to display all events a user has registered for."""
    registrations = Registration.objects.filter(user=request.user).select_related('event', 'ticket')
    return render(request, 'event/user_event_registrations.html', {'registrations': registrations})


@login_required
def cancel_event_registration(request, registration_id):
    """View to cancel a user's event registration."""
    registration = get_object_or_404(Registration, pk=registration_id, user=request.user)

    if request.method == 'POST':
        registration.status = 'cancelled'  #  Set the status to 'cancelled'
        registration.save()
        messages.success(request, "Your registration has been cancelled.")
        return redirect('event:user_event_registrations')
    return render(request, 'event/cancel_registration_confirmation.html', {'registration': registration})


def event_detail(request, event_id):
    """View for displaying details of a specific event."""
    event = get_object_or_404(Event, pk=event_id)
    return render(request, 'event/event_detail.html', {'event': event})


@login_required
@user_passes_test(is_admin)
def create_ticket(request, event_id):
    """View to create a new ticket for an event."""
    event = get_object_or_404(Event, pk=event_id)  #  Any admin can create a ticket for any event.

    if request.method == 'POST':
        name = request.POST.get('name')
        description = request.POST.get('description')
        price = request.POST.get('price')
        quantity_available = request.POST.get('quantity_available')
        status = request.POST.get('status')

        if not all([name, price, quantity_available, status]):
            messages.error(request, "All fields are required.")
            return render(request, 'event/ticket_form.html', {'event': event})

        try:
            price = float(price)
            quantity_available = int(quantity_available)
        except ValueError:
            messages.error(request, "Invalid price or quantity.")
            return render(request, 'event/ticket_form.html', {'event': event})

        ticket = Ticket.objects.create(
            event=event,
            name=name,
            description=description,
            price=price,
            quantity_available=quantity_available,
            status=status,
        )
        messages.success(request, "Ticket created successfully.")
        return redirect('event:list_tickets', event_id=event_id)
    else:
        return render(request, 'event/ticket_form.html', {'event': event})



@login_required
@user_passes_test(is_admin)
def list_tickets(request, event_id):
    """View to list all tickets for a given event."""
    event = get_object_or_404(Event, pk=event_id)  # Any admin can view tickets for any event
    tickets = Ticket.objects.filter(event=event)
    return render(request, 'event/ticket_list.html', {'tickets': tickets, 'event': event})



@login_required
@user_passes_test(is_admin)
def update_ticket(request, ticket_id):
    """View to update an existing ticket."""
    ticket = get_object_or_404(Ticket, pk=ticket_id)  # Any admin can update any ticket.
    event = ticket.event

    if request.method == 'POST':
        ticket.name = request.POST.get('name')
        ticket.description = request.POST.get('description')
        ticket.price = request.POST.get('price')
        ticket.quantity_available = request.POST.get('quantity_available')
        status = request.POST.get('status') # Get the status from the form.

        if not all([ticket.name, ticket.price, ticket.quantity_available, ticket.status]):
            messages.error(request, "All fields are required.")
            return render(request, 'event/ticket_form.html', {'event': event, 'ticket': ticket})

        try:
            ticket.price = float(ticket.price)
            ticket.quantity_available = int(ticket.quantity_available)
        except ValueError:
            messages.error(request, "Invalid price or quantity.")
            return render(request, 'event/ticket_form.html', {'event': event, 'ticket': ticket})

        ticket.status = status  # Update the ticket status
        ticket.save()
        messages.success(request, "Ticket updated successfully.")
        return redirect('event:list_tickets', event_id=event.id)
    else:
        return render(request, 'event/ticket_form.html', {'form': ticket, 'event': event, 'ticket': ticket})  # Pass ticket to template



@login_required
@user_passes_test(is_admin)
def delete_ticket(request, ticket_id):
    """View to delete a ticket."""
    ticket = get_object_or_404(Ticket, pk=ticket_id)  # Any admin can delete any ticket
    event = ticket.event

    if request.method == 'POST':
        ticket.delete()
        messages.success(request, "Ticket deleted successfully.")
        return redirect('event:list_tickets', event_id=event.id)  # Redirect to list

    return render(request, 'event/ticket_delete_confirmation.html', {'ticket': ticket, 'event': event})  # create a new template

