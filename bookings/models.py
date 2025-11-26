from django.db import models
from django.conf import settings
from django.core.exceptions import ValidationError

from shows.models import Showtime
from movies.models import Seat


# Create your models here.
class Booking(models.Model):
    STATUS_CHOICES = [
        ("Pending", "Pending"),
        ("Confirmed", "Confirmed"),
        ("Cancelled", "Cancelled"),
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    showtime = models.ForeignKey(Showtime, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="Pending")

    def __str__(self):
        return f"{self.user.username} - {self.showtime.movie.title} ({self.status})"


class Ticket(models.Model):
    booking = models.ForeignKey(
        Booking, on_delete=models.CASCADE, related_name="tickets"
    )
    seat = models.ForeignKey(Seat, on_delete=models.CASCADE)
    # qr_code = models.ImageField(upload_to="qr_codes/", blank=True, null=True)

    class Meta:
        # act as database constraint to prevent double booking of same seat for *same booking*
        unique_together = ["booking", "seat"]

    # to check if seat is already booked for the showtime
    def clean(self):
        taken_seats = Ticket.objects.filter(
            booking__showtime=self.booking.showtime,
            seat=self.seat,
            booking__status="Confirmed",
        )

        if self.booking.pk:
            taken_seats = taken_seats.exclude(booking=self.booking)

        if taken_seats.exists():
            raise ValidationError(
                f"Seat {self.seat} is already booked for this showtime."
            )

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.seat} for {self.booking.showtime}"
