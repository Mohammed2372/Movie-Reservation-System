from django.shortcuts import get_object_or_404
from django.db import transaction
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from decimal import Decimal


from movies.models import Seat
from shows.models import Showtime
from .models import Booking, Ticket
from .serializers import BookingSerializer, CreateBookingSerializer


def calculate_dynamic_price(showtime, seats):
    final_price = showtime.movie.base_price
    if showtime.start_time.hour < 12:
        discount = final_price * Decimal("0.20")
        final_price -= discount
    if seats.seat__type == "VIP":
        final_price += Decimal("10.00")
    if seats.seat_type == "Premium":
        final_price += Decimal("5.00")
    return final_price


class BookingViewSet(viewsets.ModelViewSet):
    Permission_classes = [IsAuthenticated]

    def get_serializer_class(self) -> CreateBookingSerializer | BookingSerializer:
        if self.action == "create":
            return CreateBookingSerializer
        return BookingSerializer

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

                        ticket_price = calculate_dynamic_price(
                            seat=seat, showtime=showtime
                        )

                        Ticket.objects.create(
                            booking=booking,
                            seat=seat,
                            price=ticket_price,
                        )

                return Response(
                    BookingSerializer(booking).data, status=status.HTTP_201_CREATED
                )

            except Exception as e:
                return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=["post"])
    def cancel(self, request, pk=None):
        booking = self.get_object()

        if booking.status == "Cancelled":
            return Response(
                {"error": "Booking is already cancelled."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        with transaction.atomic():
            booking.status = "Cancelled"
            booking.save()

            # delete tickets so the seats become 'Available' again in the Seat Map
            booking.seats.all().delete()

        return Response(
            {"message": "Booking cancelled successfully."}, status=status.HTTP_200_OK
        )
