from django.utils import timezone
from rest_framework import viewsets
from django_filters.rest_framework import DjangoFilterBackend


from .models import Movie
from .serializers import MovieSerializer
from .permissions import IsAdminOrReadOnly


class MovieViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer
    permission_classes = [IsAdminOrReadOnly]
    # filters
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["release_date", "genre", "is_active"]
    search_fields = ["title", "description"]
    ordering_fields = ["release_date", "duration"]

    def get_queryset(self):
        # We reuse your logic: Only show movies with future showtimes
        now = timezone.now()
        return Movie.objects.filter(showtime__start_time__gt=now).distinct()
