from django.urls import path

from .views import SeatSelectionView, BookSeats, TicketView

urlpatterns = [
    path('showtime/<int:showtime_id>/', SeatSelectionView, name='seat-selection'),
    path('showtime/<int:showtime_id>/book/', BookSeats, name='book-seats'),
    path('my-tickets/', TicketView, name='my-tickets'),
]
