from django.contrib import admin
from .models import Showtime


# Register your models here.
@admin.register(Showtime)
class ShowtimeAdmin(admin.ModelAdmin):
    list_display = ("movie", "screen", "start_time", "end_time")
    list_filter = ("screen", "start_time")
    autocomplete_fields = ["movie", "screen"]
