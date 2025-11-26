from django.contrib import admin

from .models import Movie, Theater, Screen


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
