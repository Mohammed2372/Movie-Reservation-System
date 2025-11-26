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
            "duration",
            "genre",
            "poster",
            "release_date",
        ]


class TheaterSerializer(ModelSerializer):
    class Meta:
        model = Theater
        fields = ["id", "name", "city"]


class ScreenSerializer(ModelSerializer):
    theater = TheaterSerializer(read_only=True)

    class Meta:
        model = Screen
        fields = ["id", "name", "capacity", "screen_type", "theater"]
