from rest_framework import viewsets
from .models import Movie
from .serializers import MovieSerializer
from django.utils import timezone


class MovieViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer

    def get_queryset(self):
        # We reuse your logic: Only show movies with future showtimes
        now = timezone.now()
        return Movie.objects.filter(showtime__start_time__gt=now).distinct()
