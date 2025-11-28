# 🎬 Cinema Reservation System API

A comprehensive, production-grade REST API designed to handle the full lifecycle of movie theater bookings. This system manages complex relationships between movies, screens, and showtimes while ensuring data integrity during high-concurrency booking scenarios.

## 🚀 Key Features

- **Robust Booking Engine:**

  - **Concurrency Control:** Uses atomic database transactions to prevent double-booking (race conditions) for the same seat.
  - **Dynamic Pricing:** Automatically calculates ticket prices based on VIP seat status and time-of-day discounts (e.g., Morning shows).
  - **Smart Validation:** Ensures showtimes do not overlap on the same screen.

- **Advanced Authentication & Security:**

  - **JWT Implementation:** Custom authentication system using JSON Web Tokens.
  - **HttpOnly Cookies:** Tokens are stored in secure, HttpOnly cookies to prevent XSS attacks (no local storage).
  - **Role-Based Access:** Strict permissions ensuring only Admins can manage movies/screens, while Customers have read-only access to catalog.

- **Payment & Notifications:**

  - **Stripe Integration:** Full payment lifecycle using Payment Intents.
  - **Webhooks:** Asynchronous webhook listener to automatically confirm bookings upon successful payment.
  - **Automated Emails:** Generates and sends detailed ticket receipts immediately after confirmation.

- **Architecture:**
  - **RESTful Design:** Built with Django Rest Framework (DRF) using ViewSets and Routers.
  - **Documentation:** Fully automated, interactive API documentation via Swagger UI.
  - **Test Suite:** Comprehensive unit and integration tests covering happy paths, edge cases, and security breaches.

## 🛠️ Tech Stack

- **Backend:** Python 3.10+, Django 5, Django Rest Framework
- **Database:** SQLite
- **Authentication:** SimpleJWT with Custom Cookie Middleware
- **Payments:** Stripe API
- **Documentation:** drf-spectacular (OpenAPI 3.0)

## ⚙️ Installation & Setup

1.  **Clone the repository**

    ```bash
    git clone https://github.com/Mohammed2372/Movie-Reservation-System.git
    cd Movie-Reservation-System
    ```

2.  **Create Virtual Environment & Install Dependencies**

    ```bash
    python -m venv env
    # Windows:
    env\Scripts\activate
    # Mac/Linux:
    source env/bin/activate

    pip install -r requirements.txt
    ```

3.  **Environment Variables**
    Create a `settings.py` or `.env` configuration with your Stripe keys:

    - `STRIPE_PUBLIC_KEY=pk_test_...`
    - `STRIPE_SECRET_KEY=sk_test_...`
    - `STRIPE_WEBHOOK_SECRET=whsec_...`

4.  **Database Setup**

    ```bash
    python manage.py makemigrations
    python manage.py migrate
    ```

5.  **Create Admin User**

    ```bash
    python manage.py createsuperuser
    ```

6.  **Populate Initial Data**
    The system includes a management command to auto-generate seat grids for screens.

    - First, create a Theater and Screen via Django Admin or API.
    - Then run:
      ```bash
      python manage.py generate_seats "Screen Name"
      ```

7.  **Run the Server**
    ```bash
    python manage.py runserver
    ```

## 📖 API Documentation

This project avoids manual documentation maintenance by using Swagger.
Once the server is running, visit:

**`http://127.0.0.1:8000/api/docs/`**

Here you can:

- See every endpoint (Movies, Showtimes, Auth, Bookings).
- See exactly what JSON data is required.
- Test the endpoints directly in the browser ("Try it out" button).

## 💳 Stripe Webhook Setup (Local Development)

To test payments locally:

1. Install Stripe CLI.
2. Login: stripe login
3. Forward events: stripe listen --forward-to localhost:8000/api/bookings/webhook/
4. Trigger payments via the Stripe Dashboard or CLI.
