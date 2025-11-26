from django.shortcuts import render, get_object_or_404


from shows.models import Showtime
from .models import Booking, Ticket


# Create your views here.
def SeatSelectionView(request, showtime_id):
    showtime = get_object_or_404(Showtime, id=showtime_id)
    # get all seats for the screen associated with the showtime
    seats = showtime.screen.seats.all().order_by("row", "number")

    take_seat_id = Ticket.objects.filter(
        booking__showtime=showtime, booking__status__in=["Confirmed", "Pending"]
    ).values_list("seat_id", flat=True)

    context = {
        "showtime": showtime,
        "seats": seats,
        "taken_seat_ids": take_seat_id,
    }

    return render(request, "seat_map.html", context)
