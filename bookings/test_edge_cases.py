from rest_framework.test import APITestCase
from django.urls import reverse
from rest_framework import status
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import timedelta
from decimal import Decimal

from movies.models import Movie, Theater, Screen, Seat
from shows.models import Showtime
from bookings.models import Booking


class EdgeCaseTests(APITestCase):
    def setUp(self):
        # --- 1. SETUP WORLD ---
        self.theater = Theater.objects.create(name="Edge Case Cinema", city="Test City")
        self.screen = Screen.objects.create(
            name="Screen 1", theater=self.theater, capacity=100
        )
        self.seat = Seat.objects.create(screen=self.screen, row="A", number=1)

        self.movie = Movie.objects.create(
            title="Test Movie",
            duration=120,
            release_date=timezone.now().date(),
            base_price=Decimal("10.00"),
        )

        self.showtime = Showtime.objects.create(
            movie=self.movie,
            screen=self.screen,
            start_time=timezone.now() + timedelta(days=1),
        )

        # --- 2. SETUP USERS ---
        self.user_a = User.objects.create_user(
            username="user_a", password="password123"
        )
        self.user_b = User.objects.create_user(
            username="user_b", password="password123"
        )
        self.admin_user = User.objects.create_superuser(
            username="admin", password="password123"
        )

        self.booking_url = reverse("booking-list")  # /api/bookings/

        # Helper to force login for tests
        self.client.force_authenticate(user=self.user_a)

    def test_anonymous_cannot_book(self):
        """Test that unauthenticated users get 401 or 403"""
        self.client.logout()  # Logout User A

        payload = {
            "showtime_id": self.showtime.id,
            "seats": [{"row": "A", "number": 1}],
        }
        response = self.client.post(self.booking_url, payload, format="json")

        # Should be 401 Unauthorized
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_privacy_isolation(self):
        """Test that User B cannot see User A's bookings"""
        # 1. User A books a ticket
        payload = {
            "showtime_id": self.showtime.id,
            "seats": [{"row": "A", "number": 1}],
        }
        self.client.post(self.booking_url, payload, format="json")

        # 2. Login as User B
        self.client.force_authenticate(user=self.user_b)

        # 3. Get Bookings List
        response = self.client.get(self.booking_url)

        # 4. Assert User B sees NOTHING (Count 0)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["results"]), 0)

    def test_booking_non_existent_seat(self):
        """Test booking a seat that is not in the database"""
        # Row Z, Number 99 does not exist
        payload = {
            "showtime_id": self.showtime.id,
            "seats": [{"row": "Z", "number": 99}],
        }
        response = self.client.post(self.booking_url, payload, format="json")

        # Should be 400 Bad Request
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        # Verify the error message mentions the seat issue
        self.assertIn("error", response.data)

    def test_cancellation_frees_seat(self):
        """Test that cancelling a booking makes the seat available again"""
        # 1. Book the seat
        payload = {
            "showtime_id": self.showtime.id,
            "seats": [{"row": "A", "number": 1}],
        }
        response = self.client.post(self.booking_url, payload, format="json")
        booking_id = response.data["id"]

        # 2. Cancel the booking
        # Assuming you added the @action(detail=True, methods=['post']) def cancel...
        cancel_url = reverse("booking-cancel", args=[booking_id])
        response = self.client.post(cancel_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # 3. User B tries to book the SAME seat
        self.client.force_authenticate(user=self.user_b)
        response = self.client.post(self.booking_url, payload, format="json")

        # 4. Should SUCCEED (201) because User A cancelled
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_only_admin_can_create_movies(self):
        """Test permissions for the Movies API"""
        movie_url = reverse("movie-list")  # /api/movies/
        new_movie_data = {
            "title": "Hacked Movie",
            "duration": 100,
            "release_date": "2025-01-01",
            "base_price": "10.00",
            "description": "A test movie description",
            "genre": "Action",
        }

        # 1. Try as Normal User (User A)
        response = self.client.post(movie_url, new_movie_data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        # 2. Try as Admin
        self.client.force_authenticate(user=self.admin_user)
        response = self.client.post(movie_url, new_movie_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
