from django.shortcuts import get_object_or_404
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.db import transaction

from movies.models import Seat
from shows.models import Showtime
from .models import Booking, Ticket
from .serializers import BookingSerializer, CreateBookingSerializer


# Create your views here.
class BookingViewSet(viewsets.ModelViewSet):
    Permission_classes = [IsAuthenticated]
    serializer_class = BookingSerializer

    def get_queryset(self):
        return Booking.objects.filter(user=self.request.user).order_by("-created_at")

    def create(self, request, *args, **kwargs):
        serializer = CreateBookingSerializer(data=request.data)
        if serializer.is_valid():
            showtime_id = serializer.validated_data["showtime_id"]
            seat_ids = serializer.validated_data["seats"]

            showtime = get_object_or_404(Showtime, pk=showtime_id)
            screen = showtime.screen

            try:
                with transaction.atomic():
                    # create booking
                    booking = Booking.objects.create(
                        user=request.user,
                        showtime=showtime,
                        status="Confirmed",
                    )

                    # create tickets
                    for seat in seat_ids:
                        row = seat["row"]
                        number = seat["number"]

                        try:
                            seat = Seat.objects.get(
                                screen=screen,
                                row=row,
                                number=number,
                            )
                        except Seat.DoesNotExist:
                            raise Exception(
                                f"Seat {row}{number} does not exist in {screen.name}"
                            )

                        if Ticket.objects.filter(
                            booking__showtime=showtime, seat=seat
                        ).exists():
                            raise Exception(f"Seat {row}{number} is already booked!")

                        Ticket.objects.create(booking=booking, seat=seat)

                return Response(
                    BookingSerializer(booking).data, status=status.HTTP_201_CREATED
                )

            except Exception as e:
                return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# TODO: add price for ticket based on the show, seat type, theater
