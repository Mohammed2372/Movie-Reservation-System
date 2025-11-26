from rest_framework import viewsets, views, status
from rest_framework.response import Response
from django.utils import timezone


from .models import Showtime
from .serializers import ShowtimeSerializer
from bookings.models import Ticket


# Create your views here.
class ShowtimeViewSet(viewsets.ModelViewSet):
    queryset = Showtime.objects.all().order_by("start_time")
    serializer_class = ShowtimeSerializer
    filterset_fields = ["movie"]


class SeatMapView(views.APIView):
    def get(self, request, showtime_id=None):
        try:
            showtime = Showtime.objects.get(pk=showtime_id)
        except Showtime.DoesNotExist:
            return Response(
                {"error": "Showtime not found."}, status=status.HTTP_404_NOT_FOUND
            )

        # get all seats for the screen associated with the showtime
        seats = showtime.screen.seats.all().order_by("row", "number")

        # get taken seats for the showtime
        taken_seat_ids = Ticket.objects.filter(
            booking__showtime=showtime, booking__status__in=["Confirmed", "Pending"]
        ).values_list("seat_id", flat=True)

        seat_data = []
        for seat in seats:
            seat_data.append(
                {
                    # "id": seat.id,
                    "row": seat.row,
                    "number": seat.number,
                    "status": "taken" if seat.id in taken_seat_ids else "available",
                }
            )

        return Response(seat_data)
