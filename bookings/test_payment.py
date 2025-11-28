from rest_framework.test import APITestCase
from django.urls import reverse
from rest_framework import status
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import timedelta
from decimal import Decimal
from unittest.mock import patch  # Mock Decorator to fake payment

from movies.models import Movie, Theater, Screen, Seat
from shows.models import Showtime


class PaymentFlowTest(APITestCase):
    def setUp(self):
        # 1. Setup Data (Theater, Movie, Show, User)
        self.theater = Theater.objects.create(name="Stripe Cinema", city="Test City")
        self.screen = Screen.objects.create(
            name="Screen 1", theater=self.theater, capacity=100
        )
        self.seat = Seat.objects.create(screen=self.screen, row="A", number=1)

        self.movie = Movie.objects.create(
            title="Paid Movie",
            duration=120,
            release_date=timezone.now().date(),
            base_price=Decimal("15.00"),
        )

        self.showtime = Showtime.objects.create(
            movie=self.movie,
            screen=self.screen,
            start_time=timezone.now() + timedelta(days=1),
        )

        self.user = User.objects.create_user(username="payer", password="password123")
        self.client.force_authenticate(user=self.user)
        self.url = reverse("booking-list")

    # 🟢 THE MOCK DECORATOR
    # This says: "Intercept any call to stripe.PaymentIntent.create"
    @patch("stripe.PaymentIntent.create")
    def test_booking_creates_payment_intent(self, mock_stripe_create):
        # 1. Configure the Fake Response
        # When the view calls Stripe, return this dictionary instead
        mock_stripe_create.return_value = {
            "id": "pi_fake_12345",
            "client_secret": "secret_fake_abcde",
            "amount": 1500,
            "status": "requires_payment_method",
        }

        # 2. Make the Request
        payload = {
            "showtime_id": self.showtime.id,
            "seats": [{"row": "A", "number": 1}],
        }
        response = self.client.post(self.url, payload, format="json")

        # 3. Assert Success
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # 4. Check that we got the fake secret back
        self.assertEqual(response.data["client_secret"], "secret_fake_abcde")
        self.assertEqual(response.data["status"], "Pending")

        # 5. Verify the DB saved the Fake Intent ID
        # (We need to import Booking here or inspect via response ID)
        from bookings.models import Booking

        booking = Booking.objects.get(id=response.data["id"])
        self.assertEqual(booking.stripe_payment_intent, "pi_fake_12345")

        print("\n✅ Payment Intent Mocking Test Passed!")
