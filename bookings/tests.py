from rest_framework.test import APITestCase
from django.urls import reverse
from rest_framework import status
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import timedelta
from decimal import Decimal


from movies.models import Movie, Theater, Screen, Seat
from shows.models import Showtime
from bookings.models import Booking, Ticket


class FullSystemFlowTest(APITestCase):
    def setUp(self):
        """
        Prepare the 'World' before the user arrives.
        Create Theater, Screen, Seats, Movie, and Showtime.
        """
        # 1. Create Cinema Assets
        self.theater = Theater.objects.create(
            name="Grand Test Cinema", city="Test City"
        )
        self.screen = Screen.objects.create(
            name="screen 1", theater=self.theater, capacity=100
        )

        # 2. Create 2 Seats (A1 and A2)
        self.seat1 = Seat.objects.create(
            screen=self.screen, row="A", number=1, seat_type="Regular"
        )
        self.seat2 = Seat.objects.create(
            screen=self.screen, row="A", number=2, seat_type="VIP"
        )

        # 3. Create Movie (Price $10.00)
        self.movie = Movie.objects.create(
            title="Test Movie",
            duration=120,
            release_date=timezone.now().date(),
            base_price=Decimal("10.00"),
        )

        # 4. Create Showtime (Tomorrow at 6:00 PM - No morning discount)
        tomorrow_evening = timezone.now() + timedelta(days=1)
        tomorrow_evening = tomorrow_evening.replace(hour=18, minute=0, second=0)

        self.showtime = Showtime.objects.create(
            movie=self.movie, screen=self.screen, start_time=tomorrow_evening
        )

        # URLs
        self.register_url = reverse("register")
        self.login_url = reverse("login")
        self.booking_url = reverse("booking-list")  # ViewSet standard URL name

    def test_full_user_journey(self):
        print("\n--- STARTING FULL SYSTEM TEST ---")

        # ==========================================
        # STEP 1: REGISTER
        # ==========================================
        user_data = {
            "username": "tester",
            "email": "tester@test.com",
            "password": "password123",
            "password2": "password123",
        }
        response = self.client.post(self.register_url, user_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        print("✅ Step 1: Registration Successful")

        # ==========================================
        # STEP 2: LOGIN (Get Cookies)
        # ==========================================
        login_data = {"username": "tester", "password": "password123"}
        response = self.client.post(self.login_url, login_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Check if we got cookies
        self.assertIn("access_token", response.cookies)
        print("✅ Step 2: Login Successful (Cookie Received)")

        # ==========================================
        # STEP 3: MAKE A BOOKING
        # ==========================================
        # We try to book Seat A1 (Regular) and A2 (VIP)
        booking_payload = {
            "showtime_id": self.showtime.id,
            "seats": [{"row": "A", "number": 1}, {"row": "A", "number": 2}],
        }

        # The client automatically sends the cookies from Step 2
        response = self.client.post(self.booking_url, booking_payload, format="json")

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        print("✅ Step 3: Booking Successful")

        # ==========================================
        # STEP 4: VERIFY PRICES (Dynamic Logic Check)
        # ==========================================
        # Seat A1 (Regular): $10.00
        # Seat A2 (VIP): $10.00 Base + $10.00 VIP Surcharge = $20.00

        tickets = Ticket.objects.filter(booking__user__username="tester")
        self.assertEqual(tickets.count(), 2)

        ticket_a1 = tickets.get(seat__row="A", seat__number=1)
        ticket_a2 = tickets.get(seat__row="A", seat__number=2)

        self.assertEqual(ticket_a1.price, Decimal("10.00"))
        self.assertEqual(ticket_a2.price, Decimal("20.00"))
        print("✅ Step 4: Dynamic Pricing Verified")

        # ==========================================
        # STEP 5: DOUBLE BOOKING ATTEMPT (Negative Test)
        # ==========================================
        # Create a SECOND user to try and steal the seats
        User.objects.create_user(username="thief", password="password123")
        self.client.post(
            self.login_url, {"username": "thief", "password": "password123"}
        )

        # Try to book the SAME seats
        response = self.client.post(self.booking_url, booking_payload, format="json")

        # Should fail with 400 Bad Request
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        print("✅ Step 5: Double Booking Successfully Blocked")

        print("--- TEST COMPLETED SUCCESSFULLY ---")
