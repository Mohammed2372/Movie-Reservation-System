from django.urls import path, include
from rest_framework.routers import DefaultRouter


from .views import MovieViewSet, TheaterViewSet

router = DefaultRouter()
router.register(r"movies", MovieViewSet, basename="movie")
router.register(r"theaters", TheaterViewSet, basename="theater")

urlpatterns = [
    path("", include(router.urls)),
]
