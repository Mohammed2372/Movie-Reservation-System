from rest_framework import serializers
from rest_framework.serializers import ModelSerializer
from drf_spectacular.utils import extend_schema


from .models import Booking, Ticket
from shows.serializers import ShowtimeSerializer


class TicketSerializer(ModelSerializer):
    seat_str = serializers.SerializerMethodField()

    class Meta:
        model = Ticket
        fields = [
            # "id",
            # "seat",
            "seat_str",
            "price",
        ]

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


class BookingListSerializer(ModelSerializer):
    # flattening movie data
    movie_title = serializers.CharField(source="showtime.movie.title")
    poster = serializers.ImageField(source="showtime.movie.poster")

    # flattening cinema/screen data
    theater_name = serializers.CharField(source="showtime.screen.theater.name")
    screen_name = serializers.CharField(source="showtime.screen.name")

    # formatting time
    start_time = serializers.DateTimeField(source="showtime.start_time")

    # using ticket serializer to make it simple
    tickets = TicketSerializer(many=True, read_only=True)

    # calculate total price
    total_price = serializers.SerializerMethodField()

    class Meta:
        model = Booking
        # only selecting important fields to show
        fields = [
            "id",
            "status",
            "movie_title",
            "poster",
            "theater_name",
            "screen_name",
            "start_time",
            "tickets",
            "total_price",
        ]

    def get_total_price(self, obj):
        return str(sum(ticket.price for ticket in obj.tickets.all()))
