from django.contrib import admin

from .models import Movie, Theater, Screen, Seat


# Register your models here.
class ScreenInline(admin.TabularInline):
    model = Screen
    extra = 1


@admin.register(Theater)
class TheaterAdmin(admin.ModelAdmin):
    inlines = [ScreenInline]
    list_display = ("name", "city")


@admin.register(Movie)
class MovieAdmin(admin.ModelAdmin):
    list_display = ("title", "release_date", "duration", "is_active")
    search_fields = ("title", "genre", "release_data")


@admin.register(Screen)
class ScreenAdmin(admin.ModelAdmin):
    list_display = ("name", "theater", "capacity", "screen_type")
    search_fields = ("name", "theater__name")


@admin.register(Seat)
class SeatAdmin(admin.ModelAdmin):
    list_display = ("screen", "row", "number", "seat_type")
    list_filter = ("seat_type", "screen")
    search_fields = ("row", "screen__name")
