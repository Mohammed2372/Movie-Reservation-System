from django.urls import path, include
from rest_framework.routers import DefaultRouter


from .views import BookingViewSet, stripe_webhook


router = DefaultRouter()
router.register(r"bookings", BookingViewSet, basename="booking")

urlpatterns = [
    path("", include(router.urls)),
    path("webhook/", stripe_webhook, name="stripe-webhook"),
]
