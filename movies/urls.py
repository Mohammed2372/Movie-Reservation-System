from django.urls import path, include
from rest_framework.routers import DefaultRouter


from .views import MovieViewSet, TheaterViewSet, ScreenViewSet

router = DefaultRouter()
router.register(r"movies", MovieViewSet, basename="movie")
router.register(r"theaters", TheaterViewSet, basename="theater")
router.register(r"screens", ScreenViewSet, basename="screen")

urlpatterns = [
    path("", include(router.urls)),
]
