from django.db.models.manager import BaseManager
from django.utils import timezone
from rest_framework import viewsets, filters
from django_filters.rest_framework import DjangoFilterBackend


from .models import Movie, Theater, Screen
from .serializers import (
    MovieSerializer,
    TheaterSerializer,
    ScreenReadSerializer,
    ScreenWriteSerializer,
)
from .permissions import IsAdminOrReadOnly


class MovieViewSet(viewsets.ModelViewSet):
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer
    permission_classes = [IsAdminOrReadOnly]
    # filters
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ["release_date", "genre", "is_active"]
    search_fields = ["title", "description"]
    ordering_fields = ["release_date", "duration"]

    def get_queryset(self) -> BaseManager[Movie]:
        # if admin, show all movies
        if self.request.user.is_staff:
            return Movie.objects.all()

        # if customer, show only the with future showtime
        now = timezone.now()
        return Movie.objects.filter(showtime__start_time__gt=now).distinct()


class TheaterViewSet(viewsets.ModelViewSet):
    queryset = Theater.objects.all()
    serializer_class = TheaterSerializer
    permission_classes = [IsAdminOrReadOnly]
    # filters
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ["city"]
    search_fields = ["name", "address"]
    ordering_fields = ["name", "city"]


class ScreenViewSet(viewsets.ModelViewSet):
    queryset = Screen.objects.all()
    permission_classes = [IsAdminOrReadOnly]

    def get_serializer_class(self) -> ScreenReadSerializer | ScreenWriteSerializer:
        if self.action in ["list", "retrieve"]:
            return ScreenReadSerializer
        return ScreenWriteSerializer
