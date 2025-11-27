from django.utils import timezone
from rest_framework import viewsets


from .models import Movie
from .serializers import MovieSerializer
from .permissions import IsAdminOrReadOnly


class MovieViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer
    permission_classes = [IsAdminOrReadOnly]

    def get_queryset(self):
        # We reuse your logic: Only show movies with future showtimes
        now = timezone.now()
        return Movie.objects.filter(showtime__start_time__gt=now).distinct()
