from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ShowtimeViewSet, SeatMapView

router = DefaultRouter()
router.register(r"showtimes", ShowtimeViewSet, basename="showtimes")

urlpatterns = [
    path("", include(router.urls)),
    # Custom endpoint for the seat map
    path("showtimes/<int:showtime_id>/seats/", SeatMapView.as_view(), name="seat_map_api"),
]
