from django.urls import path

from .views import SeatSelectionView

urlpatterns = [
    path('showtime/<int:showtime_id>/', SeatSelectionView, name='seat_selection'),
]
