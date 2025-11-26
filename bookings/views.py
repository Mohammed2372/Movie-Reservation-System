from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.contrib import messages


from movies.models import Seat
from shows.models import Showtime
from .models import Booking, Ticket


# Create your views here.
@login_required(login_url="admin/login/")  # NOTE: redirect to admin login for now
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
        "taken_seat_ids": list(take_seat_id),
    }

    return render(request, "seat_map.html", context)


# TODO: redirect to login page for users
@login_required(login_url="admin/login/")  # NOTE: redirect to admin login for now
def BookSeats(request, showtime_id):
    if request.method == "POST":
        # get selected seat ids of show from the form
        showtime = get_object_or_404(Showtime, pk=showtime_id)

        raw_selected_seat_ids = request.POST.get("seat_ids", "")

        if not raw_selected_seat_ids:
            messages.error(request, "No seats selected.")
            return redirect("seat-selection", showtime_id=showtime_id)

        selected_seat_ids = raw_selected_seat_ids.split(",")
        selected_seat_ids = [seat_id for seat_id in selected_seat_ids if seat_id]

        try:
            with transaction.atomic():
                # create the booking
                booking = Booking.objects.create(
                    user=request.user,
                    showtime=showtime,
                    status="Confirmed",  # NOTE: auto-confirming for now
                )

                # create tickets for each selected seat
                for seat_id in selected_seat_ids:
                    seat = get_object_or_404(Seat, pk=seat_id)
                    ticket = Ticket(
                        booking=booking,
                        seat=seat,
                        # TODO: add price for ticket based on the show, seat type, theater
                    )
                    ticket.save()

            messages.success(request, "Booking Successful!")
            return redirect("seat-selection", showtime_id=showtime_id)
        except Exception as e:
            messages.error(request, f"Booking Failed: {str(e)}")
            return redirect("seat-selection", showtime_id=showtime_id)
    return redirect("seat-selection", showtime_id=showtime_id)


def TicketView(request):
    # get all bookings for the user
    bookings = (
        Booking.objects.filter(user=request.user)
        .select_related("showtime__movie", "showtime__screen")
        .prefetch_related("tickets__seat")
        .order_by("-created_at")
    )

    context = {"bookings": bookings}
    
    return render(request, "my_tickets.html", context)
