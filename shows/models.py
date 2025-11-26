from django.db import models
from django.core.exceptions import ValidationError
from django.utils import timezone
from datetime import timedelta
from django.db.models import Q  # for better queries

from movies.models import Movie, Screen


# Create your models here.
class Showtime(models.Model):
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    screen = models.ForeignKey(Screen, on_delete=models.CASCADE)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField(
        blank=True, null=True, help_text="It will be automatically calculated."
    )

    def save(self, *args, **kwargs):
        if self.movie and self.start_time:
            duration = timedelta(minutes=self.movie.duration)
            cleaning_time = timedelta(minutes=15)
            self.end_time = self.start_time + duration + cleaning_time
        super().save(*args, **kwargs)

    # Check for overlapping showtimes before saving or updating
    def clean(self):
        if not self.movie or not self.start_time:
            return

        duration = timedelta(minutes=self.movie.duration)
        cleaning_time = timedelta(minutes=15)
        predicted_end = self.start_time + duration + cleaning_time

        overlapping_shows = Showtime.objects.filter(
            Q(screen=self.screen)
            & Q(start_time__lt=predicted_end)
            & Q(end_time__gt=self.start_time)
        ).exclude(pk=self.pk)  # Exclude self

        if overlapping_shows.exists():
            conflict = overlapping_shows.first()
            raise ValidationError(
                f"Overlap detected! {conflict.movie.title} is playing from "
                f"{conflict.start_time.strftime('%H:%M')} to {conflict.end_time.strftime('%H:%M')}."
            )

        def __str__(self):
            local_time = timezone.localtime(self.start_time)
            return f"{self.movie.title} at {local_time.strftime('%Y-%m-%d %H:%M')} on Screen: {self.screen.name}"
