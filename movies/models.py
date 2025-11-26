from django.db import models


# Create your models here.
class Movie(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    genre = models.CharField(max_length=50)
    duration = models.PositiveIntegerField(help_text="Duration in minutes")
    rating = models.ValueRange(1, 5)
    poster = models.ImageField(upload_to="images/", blank=True, null=True)
    trailer_url = models.URLField(blank=True, null=True)
    release_date = models.DateField()
    is_active = models.BooleanField(
        default=True, help_text="Is this movie currently showing?"
    )

    def __str__(self):
        return self.title


class Theater(models.Model):
    name = models.CharField(max_length=100)
    address = models.TextField()
    city = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.name} at {self.city}"


class Screen(models.Model):
    SCREEN_TYPE_CHOICES = [
        ("2D", "Standard 2D"),
        ("3D", "3D"),
        ("IMAX", "IMAX"),
    ]

    name = models.CharField(max_length=50)
    theater = models.ForeignKey(
        Theater, on_delete=models.CASCADE, related_name="screens"
    )
    capacity = models.PositiveIntegerField(help_text="Total number of seats")
    screen_type = models.CharField(max_length=10, choices=SCREEN_TYPE_CHOICES)

    def __str__(self):
        return f"{self.name} at {self.theater}"
