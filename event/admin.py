from django.contrib import admin
from .models import Category, Event, Ticket, Registration, EventAnalytics

admin.site.register(Category)
admin.site.register(Event)
admin.site.register(Ticket)
admin.site.register(Registration)
admin.site.register(EventAnalytics)