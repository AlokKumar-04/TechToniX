from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from event.models import Event, Category, Ticket, Registration
from event.forms import EventForm, TicketFormSet

def is_organizer_or_admin(user):
    return user.is_staff or user.role == 'organizer'

def event_list(request):
    events = Event.objects.filter(status='approved').order_by('date')
    context = {
        'events': events,
    }
    return render(request, 'event/event_list.html', context)

def event_detail(request, event_id):
    event = get_object_or_404(Event, pk=event_id, status='approved')
    tickets = Ticket.objects.filter(event=event)
    context = {
        'event': event,
        'tickets': tickets,
    }
    return render(request, 'event/event_detail.html', context)

@login_required
@user_passes_test(is_organizer_or_admin)
def event_create(request):
    if request.method == 'POST':
        form = EventForm(request.POST, request.FILES)
        if form.is_valid():
            event = form.save(commit=False)
            event.organizer = request.user
            event.save()

            # Now that the event is saved, associate it with the formset
            ticket_formset = TicketFormSet(request.POST, instance=event)
            if ticket_formset.is_valid():
                ticket_formset.save()
                messages.success(request, 'Event created successfully and is pending approval.')
                return redirect('event:event_detail', event_id=event.id)
            else:
                messages.error(request, 'There was an error saving the tickets. Please correct the form below.')
                context = {
                    'form': form,
                    'ticket_formset': ticket_formset,
                }
                return render(request, 'event/event_form.html', context)
        else:
            ticket_formset = TicketFormSet(request.POST) # Initialize even if event form is invalid for error display
            messages.error(request, 'There was an error creating the event. Please correct the form below.')
            context = {
                'form': form,
                'ticket_formset': ticket_formset,
            }
            return render(request, 'event/event_form.html', context)
    else:
        form = EventForm()
        ticket_formset = TicketFormSet()
        context = {
            'form': form,
            'ticket_formset': ticket_formset,
        }
        return render(request, 'event/event_form.html', context)

@login_required
@user_passes_test(is_organizer_or_admin)
def organizer_dashboard(request):
    organized_events = Event.objects.filter(organizer=request.user).order_by('-created_at')
    context = {
        'organized_events': organized_events,
    }
    return render(request, 'event/organizer_dashboard.html', context)





@login_required
def register_for_event(request, event_id, ticket_id):
    event = get_object_or_404(Event, pk=event_id, status='approved')
    ticket = get_object_or_404(Ticket, pk=ticket_id, event=event)
    if request.method == 'POST':
        if ticket.quantity_available > 0:
            Registration.objects.create(user=request.user, event=event, ticket=ticket)
            ticket.quantity_available -= 1
            ticket.save()
            messages.success(request, f'You have successfully registered for {event.name} - {ticket.name}.')
            return redirect('event:user_registrations')
        else:
            messages.error(request, f'Sorry, {ticket.name} tickets are sold out.')
            return redirect('event:event_detail', event_id=event_id)
    else:
        context = {
            'event': event,
            'ticket': ticket,
        }
        return render(request, 'event/register.html', context)
    




@login_required
def user_registrations(request):
    registrations = Registration.objects.filter(user=request.user).order_by('-registration_date')
    context = {
        'registrations': registrations,
    }
    return render(request, 'event/user_registrations.html', context)





@login_required
def cancel_registration(request, registration_id):
    registration = get_object_or_404(Registration, pk=registration_id, user=request.user)
    event = registration.event
    ticket = registration.ticket
    if request.method == 'POST':
        registration.delete()
        if ticket:
            ticket.quantity_available += 1
            ticket.save()
        messages.success(request, f'Your registration for {event.name} has been cancelled.')
        return redirect('event:user_registrations')
    else:
        context = {
            'registration': registration,
        }
        return render(request, 'event/cancel_registration.html', context)
    




@login_required
@user_passes_test(is_organizer_or_admin)
def event_edit(request, event_id):
    event = get_object_or_404(Event, pk=event_id, organizer=request.user)
    if request.method == 'POST':
        form = EventForm(request.POST, request.FILES, instance=event)
        ticket_formset = TicketFormSet(request.POST, instance=event)
        if form.is_valid() and ticket_formset.is_valid():
            form.save()
            ticket_formset.save()
            messages.success(request, 'Event details updated successfully.')
            return redirect('event:event_detail', event_id=event.id)
        else:
            messages.error(request, 'There was an error updating the event. Please correct the form below.')
            context = {
                'form': form,
                'ticket_formset': ticket_formset,
                'event': event,
            }
            return render(request, 'event/event_form.html', context)
    else:
        form = EventForm(instance=event)
        ticket_formset = TicketFormSet(instance=event)
        context = {
            'form': form,
            'ticket_formset': ticket_formset,
            'event': event,
        }
        return render(request, 'event/event_form.html', context)
    



    

@login_required
@user_passes_test(is_organizer_or_admin)
def event_delete(request, event_id):
    event = get_object_or_404(Event, pk=event_id, organizer=request.user)
    if request.method == 'POST':
        event.delete()
        messages.success(request, f'Event "{event.name}" has been deleted.')
        return redirect('event:organizer_dashboard')
    else:
        context = {
            'event': event,
        }
        return render(request, 'event/event_delete_confirm.html', context)