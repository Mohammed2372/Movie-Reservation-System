# 🎬 Cinema Reservation System API

A production-grade RESTful API for a movie theater booking system built with Django Rest Framework. Features JWT authentication, atomic transactions, PostgreSQL, Docker, Stripe integration, and comprehensive concurrency handling for high-traffic ticket bookings.

**Project Inspiration:** [roadmap.sh/projects/movie-reservation-system](https://roadmap.sh/projects/movie-reservation-system)

## 🚀 Key Features

### 🔐 Security & Authentication

- **JWT via HttpOnly Cookies:** Authentication uses JSON Web Tokens stored in HttpOnly cookies. This prevents XSS attacks (as JavaScript cannot read the token) while maintaining stateless authentication.
- **Role-Based Access Control (RBAC):** Custom permissions ensure only Admins can modify the catalog (Movies, Screens), while customers have read-only access to schedules.

### 🎟️ Booking Engine

- **Race Condition Prevention** – Uses `transaction.atomic()` to handle concurrent seat bookings safely
- **Smart Scheduling Validation** – Prevents overlapping showtimes on the same screen
- **Dynamic Pricing Algorithm**
  - 20% discount for morning shows
  - Tiered pricing for VIP and Premium seats
  - Real-time price calculation at checkout

### 💳 Payments & Notifications

- **Stripe Integration:** Full implementation of Stripe **Payment Intents** API.
- **Asynchronous Webhooks:** A secure webhook listener waits for Stripe's "Payment Succeeded" signal to confirm bookings in real-time, regardless of frontend connectivity.
- **Automated Emails:** Generates and sends a detailed ticket receipt email immediately upon payment confirmation.

### 📚 Developer Experience

- **Interactive API Documentation** – Swagger UI powered by drf-spectacular
- **Comprehensive Test Suite** – Unit and integration tests covering happy paths, edge cases, and security scenarios
- **Docker Support** – One-command setup with docker-compose

---

## 🛠️ Tech Stack

| Category             | Technology                            |
| -------------------- | ------------------------------------- |
| **Backend**          | Python 3.11+, Django 5.x              |
| **API Framework**    | Django Rest Framework (DRF)           |
| **Database**         | PostgreSQL (Production), SQLite (Dev) |
| **Authentication**   | Simple JWT with HttpOnly cookies      |
| **Payments**         | Stripe API v3                         |
| **Documentation**    | drf-spectacular (OpenAPI 3.0)         |
| **Containerization** | Docker, Docker Compose                |

---

## 📂 Project Structure

```
movie-reservation-system/
├── accounts/              # User authentication & JWT logic
├── bookings/              # Booking engine, payments, webhooks
├── movies/                # Movie catalog & theater management
├── shows/                 # Showtimes, screens, seat maps
├── manage.py
├── Dockerfile
├── docker-compose.yml
└── requirements.txt
```

---

## ⚙️ Setup & Installation

### Option 1: Docker (Recommended)

**`Prerequisites:`** Docker and Docker Compose installed

1. **Clone the repository**

```bash
git clone https://github.com/Mohammed2372/Movie-Reservation-System.git
cd Movie-Reservation-System
```

2. **Configure environment variables**

Create a `.env` file in the project root:

```env
DEBUG=1
ALLOWED_HOSTS=localhost,127.0.0.1,0.0.0.0
SECRET_KEY=your-secret-key-here
POSTGRES_DB=movie_db
POSTGRES_USER=movie_user
POSTGRES_PASSWORD=your-secure-password
DATABASE_URL=postgres://movie_user:your-secure-password@db:5432/movie_db
STRIPE_PUBLIC_KEY=pk_test_...
STRIPE_SECRET_KEY=sk_test_...
STRIPE_WEBHOOK_SECRET=whsec_...
```

3. **Start the application**

```bash
docker-compose up --build
```

The API will be available at **http://localhost:8000/api/docs/**

4. **Initialize the database**

In a new terminal window:

```bash
# Create admin user
docker-compose exec web python manage.py createsuperuser

# Generate seat layout for a screen (after creating it via admin panel)
docker-compose exec web python manage.py generate_seats "Screen Name"
```

---

### Option 2: Local Development

**Prerequisites:** Python 3.11+, PostgreSQL (or use SQLite for dev)

1. **Clone and setup virtual environment**

```bash
git clone https://github.com/Mohammed2372/Movie-Reservation-System.git
cd Movie-Reservation-System

# Create and activate virtual environment
python -m venv env

# Windows
env\Scripts\activate

# macOS/Linux
source env/bin/activate
```

2. **Install dependencies**

```bash
pip install -r requirements.txt
```

3. **Configure environment**

Add these settings to your `settings.py` or create a `.env` file:

```python
STRIPE_PUBLIC_KEY = 'pk_test_...'
STRIPE_SECRET_KEY = 'sk_test_...'
STRIPE_WEBHOOK_SECRET = 'whsec_...'
```

4. **Setup database**

```bash
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
```

5. **Generate initial data**

Create a theater and screen via Django Admin (`/admin/`), then:

```bash
python manage.py generate_seats "Screen Name"
```

6. **Run development server**

```bash
python manage.py runserver
```

Visit **http://127.0.0.1:8000/api/docs/** for API documentation.

---

## 📖 API Documentation

This project uses **Swagger UI** for interactive API documentation.

**Access it at:** `http://127.0.0.1:8000/api/docs/`

**Features:**

- Browse all endpoints (Authentication, Movies, Showtimes, Bookings)
- View request/response schemas
- Test endpoints directly in the browser with the "Try it out" feature
- Auto-generated from code annotations (no manual updates needed)

**Key Endpoints:**

- `POST /api/accounts/register/` – User registration
- `POST /api/accounts/login/` – JWT authentication
- `GET /api/movies/` – List all movies
- `GET /api/shows/` – Get showtimes
- `POST /api/bookings/create/` – Create a booking
- `POST /api/bookings/payment/` – Process payment
- `POST /api/bookings/webhook/` – Stripe webhook handler

---

## 💳 Stripe Webhook Setup (Local Development)

To test payment webhooks locally:

1. **Install Stripe CLI**

   Download from [stripe.com/docs/stripe-cli](https://stripe.com/docs/stripe-cli)

2. **Authenticate**

```bash
stripe login
```

3. **Forward webhook events to your local server**

```bash
stripe listen --forward-to localhost:8000/api/bookings/webhook/
```

4. **Trigger test events**

```bash
stripe trigger payment_intent.succeeded
```

The CLI will display your webhook signing secret – add it to your `.env` file as `STRIPE_WEBHOOK_SECRET`.

---

## 🔒 Security Considerations

- JWT tokens stored in HttpOnly cookies (not accessible via JavaScript)
- CSRF protection enabled for state-changing operations
- Database transactions prevent race conditions in booking flow
- Stripe webhook signatures verified before processing
- Environment variables for all sensitive credentials
- Input validation on all API endpoints

---
