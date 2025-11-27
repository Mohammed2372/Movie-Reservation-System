from rest_framework import serializers
from rest_framework.serializers import ModelSerializer
from drf_spectacular.utils import extend_schema


from .models import Booking, Ticket
from shows.serializers import ShowtimeSerializer


class TicketSerializer(ModelSerializer):
    seat_str = serializers.SerializerMethodField()

    class Meta:
        model = Ticket
        fields = ["id", "seat", "seat_str"]

    @extend_schema(serializers.CharField())
    def get_seat_str(self, obj):
        return f"{obj.seat.row}{obj.seat.number}"


class BookingSerializer(ModelSerializer):
    # used for listing 'my tickets' for a user
    showtime = ShowtimeSerializer(read_only=True)
    tickets = TicketSerializer(many=True, read_only=True)

    class Meta:
        model = Booking
        fields = ["id", "showtime", "status", "created_at", "tickets"]


# helper serializer
class SeatSelectorSerializer(serializers.Serializer):
    row = serializers.CharField()
    number = serializers.IntegerField()


class CreateBookingSerializer(serializers.Serializer):
    showtime_id = serializers.IntegerField()
    seats = serializers.ListField(
        child=SeatSelectorSerializer(),
        help_text="List of seats with row('A', 'B', etc) and number(1, 2, etc)",
    )
    status = serializers.CharField()
    created_at = serializers.DateTimeField(read_only=True)
