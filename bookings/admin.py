from django.contrib import admin
from .models import Booking, Ticket


# Register your models here.
class TicketInline(admin.TabularInline):
    model = Ticket
    extra = 1


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    inlines = [TicketInline]
    list_display = ("user", "showtime__movie", "status", "created_at")
    list_filter = ("status", "created_at")
    search_fields = ("user__username", "showtime__movie__title")


@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):
    list_display = ("booking", "seat")
