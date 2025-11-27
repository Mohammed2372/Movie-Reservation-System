from rest_framework import viewsets, views, status
from rest_framework.response import Response
from rest_framework import serializers
from django.utils import timezone
from drf_spectacular.utils import extend_schema, inline_serializer
from django_filters.rest_framework import DjangoFilterBackend, filters


from .models import Showtime
from .serializers import ShowtimeSerializer
from bookings.models import Ticket


# Create your views here.
class ShowtimeViewSet(viewsets.ModelViewSet):
    queryset = Showtime.objects.filter(start_time__gt=timezone.now())
    serializer_class = ShowtimeSerializer
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ["movie", "fields"]
    ordering_fields = ["start_time"]


class SeatMapView(views.APIView):
    @extend_schema(
        responses=inline_serializer(
            name="SeatMapResponse",
            fields={
                "id": serializers.IntegerField(),
                "row": serializers.CharField(),
                "number": serializers.IntegerField(),
                "status": serializers.CharField(),
            },
            many=True,
        )
    )
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
