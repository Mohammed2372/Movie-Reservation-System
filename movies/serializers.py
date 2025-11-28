from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from .models import Movie, Screen, Theater, Seat


class MovieSerializer(ModelSerializer):
    class Meta:
        model = Movie
        fields = [
            "id",
            "title",
            "description",
            "base_price",
            "duration",
            "genre",
            "poster",
            "release_date",
        ]


class TheaterSerializer(ModelSerializer):
    class Meta:
        model = Theater
        fields = ["id", "name", "city"]


class ScreenWriteSerializer(ModelSerializer):
    theater_id = serializers.PrimaryKeyRelatedField(
        queryset=Theater.objects.all(), required=True, source="theater"
    )

    class Meta:
        model = Screen
        fields = ["id", "name", "capacity", "screen_type", "theater_id"]


class ScreenReadSerializer(ModelSerializer):
    theater = TheaterSerializer(read_only=True)

    class Meta:
        model = Screen
        fields = ["id", "name", "capacity", "screen_type", "theater"]
