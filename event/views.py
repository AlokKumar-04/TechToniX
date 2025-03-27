from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib import messages
from .models import Event, Category, Ticket, Registration
from .forms import EventForm, TicketFormSet

# Helper function to check if a user is an organizer or admin
def is_organizer_or_admin(user):
    return user.is_staff or user.role == 'organizer'

# Mixin to enforce organizer or admin access
class OrganizerOrAdminRequiredMixin(LoginRequiredMixin, UserPassesTestMixin):
    def test_func(self):
        return is_organizer_or_admin(self.request.user)

    def handle_no_permission(self):
        messages.error(self.request, "You do not have permission to access this page.")
        return redirect('event:event_list') # Redirect to a public page

class EventListView(View):
    template_name = 'event/event_list.html'

    def get(self, request):
        events = Event.objects.filter(status='approved').order_by('date')
        categories = Category.objects.all()
        context = {
            'events': events,
            'categories': categories,
        }
        return render(request, self.template_name, context)

class EventCategoryListView(View):
    template_name = 'event/event_list.html'

    def get(self, request, category_id):
        category = get_object_or_404(Category, id=category_id)
        events = Event.objects.filter(category=category, status='approved').order_by('date')
        categories = Category.objects.all()
        context = {
            'events': events,
            'categories': categories,
            'current_category': category,
        }
        return render(request, self.template_name, context)

class EventDetailView(View):
    template_name = 'event/event_detail.html'

    def get(self, request, event_id):
        event = get_object_or_404(Event, id=event_id, status='approved')
        tickets = event.tickets.all()
        context = {
            'event': event,
            'tickets': tickets,
        }
        return render(request, self.template_name, context)

class OrganizerDashboardView(OrganizerOrAdminRequiredMixin, View):
    template_name = 'event/organizer_dashboard.html'

    def get(self, request):
        organized_events = Event.objects.filter(organizer=request.user).order_by('-created_at')
        context = {
            'organized_events': organized_events,
        }
        return render(request, self.template_name, context)

class EventCreateView(OrganizerOrAdminRequiredMixin, View):
    template_name = 'event/event_form.html'

    def get(self, request):
        form = EventForm()
        ticket_formset = TicketFormSet()
        context = {
            'form': form,
            'ticket_formset': ticket_formset,
        }
        return render(request, self.template_name, context)

    def post(self, request):
        form = EventForm(request.POST, request.FILES)
        ticket_formset = TicketFormSet(request.POST, instance=Event()) # Associate with a new Event instance initially
        if form.is_valid() and ticket_formset.is_valid():
            event = form.save(commit=False)
            event.organizer = request.user
            event.save()
            ticket_formset.instance = event # Now associate tickets with the saved event
            ticket_formset.save()
            messages.success(request, 'Event created successfully and is pending approval.')
            return redirect('event:event_detail', event_id=event.id)
        else:
            messages.error(request, 'There was an error creating the event. Please correct the form below.')
            context = {
                'form': form,
                'ticket_formset': ticket_formset,
            }
            return render(request, self.template_name, context)

class EventEditView(OrganizerOrAdminRequiredMixin, View):
    template_name = 'event/event_form.html'

    def get(self, request, event_id):
        event = get_object_or_404(Event, id=event_id, organizer=request.user)
        form = EventForm(instance=event)
        ticket_formset = TicketFormSet(instance=event)
        context = {
            'form': form,
            'ticket_formset': ticket_formset,
            'is_edit': True,
            'event_id': event_id,
        }
        return render(request, self.template_name, context)

    def post(self, request, event_id):
        event = get_object_or_404(Event, id=event_id, organizer=request.user)
        form = EventForm(request.POST, request.FILES, instance=event)
        ticket_formset = TicketFormSet(request.POST, instance=event)
        if form.is_valid() and ticket_formset.is_valid():
            form.save()
            ticket_formset.save()
            messages.success(request, 'Event updated successfully.')
            return redirect('event:event_detail', event_id=event.id)
        else:
            messages.error(request, 'There was an error updating the event. Please correct the form below.')
            context = {
                'form': form,
                'ticket_formset': ticket_formset,
                'is_edit': True,
                'event_id': event_id,
            }
            return render(request, self.template_name, context)

class EventDeleteView(OrganizerOrAdminRequiredMixin, View):
    def get(self, request, event_id):
        event = get_object_or_404(Event, id=event_id, organizer=request.user)
        context = {'event': event}
        return render(request, 'event/event_confirm_delete.html', context)

    def post(self, request, event_id):
        event = get_object_or_404(Event, id=event_id, organizer=request.user)
        event.delete()
        messages.success(request, 'Event deleted successfully.')
        return redirect('event:organizer_dashboard')