# 🎬 Cinema Reservation System API

A production-grade, RESTful API for a movie theater booking system. This project manages the full lifecycle of a cinema ecosystem—from scheduling movies and managing screens to handling high-concurrency ticket bookings and processing secure payments.

project idea: [movie-reservation-system](https://roadmap.sh/projects/movie-reservation-system)

## Built with **Django Rest Framework (DRF)**, featuring secure JWT authentication, atomic database transactions, and third-party integrations (Stripe).

## 🚀 Key Features

### 🔐 Security & Authentication

- **JWT via HttpOnly Cookies:** Authentication uses JSON Web Tokens stored in HttpOnly cookies. This prevents XSS attacks (as JavaScript cannot read the token) while maintaining stateless authentication.
- **Role-Based Access Control (RBAC):** Custom permissions ensure only Admins can modify the catalog (Movies, Screens), while customers have read-only access to schedules.

### 🎟️ Booking Engine (The Core Logic)

- **Concurrency Handling:** Utilizes `transaction.atomic()` to ensure that if two users try to book the same seat at the exact same millisecond, only one succeeds. This prevents "Race Conditions."
- **Smart Scheduling:** Validation logic prevents scheduling overlapping movies on the same screen.
- **Dynamic Pricing:** automatically calculates ticket prices based on business rules:
  - _Time-of-Day:_ 20% discount for morning shows.
  - _Seat Tier:_ Surcharges for VIP and Premium seats.

### 💳 Payments & Notifications

- **Stripe Integration:** Full implementation of Stripe **Payment Intents** API.
- **Asynchronous Webhooks:** A secure webhook listener waits for Stripe's "Payment Succeeded" signal to confirm bookings in real-time, regardless of frontend connectivity.
- **Automated Emails:** Generates and sends a detailed ticket receipt email immediately upon payment confirmation.

### 📚 Documentation & Testing

- **Automated Documentation:** Fully interactive API documentation via **Swagger UI** (drf-spectacular).
- **Comprehensive Testing:** A robust test suite covering:
  - Happy Paths (Booking flow).
  - Edge Cases (Double booking, non-existent seats).
  - Security (Unauthorized access attempts).

---

## 🛠️ Tech Stack

| Category              | Technology                               |
| :-------------------- | :--------------------------------------- |
| **Backend Framework** | Python 3.11+, Django 5                   |
| **API Framework**     | Django Rest Framework (DRF)              |
| **Database**          | SQLite (Dev) / PostgreSQL                |
| **Authentication**    | SimpleJWT (Custom Cookie Implementation) |
| **Payment Gateway**   | Stripe API                               |
| **Documentation**     | drf-spectacular (OpenAPI 3.0)            |
| **DevOps**            | Docker, Docker Compose                   |

---

## ⚙️ Setup & Installation

Follow these steps to run the API locally.

### 1. Clone and Install

```bash
git clone https://github.com/Mohammed2372/Movie-Reservation-System.git
cd Movie-Reservation-System

# Create Virtual Environment
python -m venv env

# Activate (Windows)
env\Scripts\activate
# Activate (Mac/Linux)
source env/bin/activate

# Install Dependencies
pip install -r requirements.txt
```

### 2. **Environment Variables**

Create a `settings.py` or `.env` configuration with your Stripe keys:

- `STRIPE_PUBLIC_KEY=pk_test_...`
- `STRIPE_SECRET_KEY=sk_test_...`
- `STRIPE_WEBHOOK_SECRET=whsec_...`

### 3. **Database Setup**

```bash
python manage.py makemigrations
python manage.py migrate
```

### 4. **Create Admin User**

```bash
python manage.py createsuperuser
```

### 5. **Populate Initial Data**

The system includes a management command to auto-generate seat grids for screens.

- First, create a Theater and Screen via Django Admin or API.
- Then run:
  ```bash
  python manage.py generate_seats "Screen Name"
  ```

### 6. **Run the Server**

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
