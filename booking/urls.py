from django.urls import path

from booking.views import (
    HomeView,
    BarberListView,
    BarberDetailView,
    ServiceListView,
    BookingListView,
    BookingCreateView,
    RegisterView,
    BookingCancellationView,
    BarberBookingListView,
    BookingStatusUpdateView,
)

app_name = "booking"

urlpatterns = [
    path("", HomeView.as_view(), name="home-page"),
    path("barbers/", BarberListView.as_view(), name="barber-list"),
    path(
        "barbers/<int:pk>/", BarberDetailView.as_view(), name="barber-detail"
    ),
    path("services/", ServiceListView.as_view(), name="service-list"),
    path("bookings/", BookingListView.as_view(), name="booking-list"),
    path(
        "barber/bookings/",
        BarberBookingListView.as_view(),
        name="barber-booking-list",
    ),
    path(
        "bookings/<int:pk>/cancel/",
        BookingCancellationView.as_view(),
        name="booking-cancel",
    ),
    path(
        "barber/bookings/<int:pk>/update-status/",
        BookingStatusUpdateView.as_view(),
        name="booking-update-status",
    ),
    path(
        "booking/create/", BookingCreateView.as_view(), name="booking-create"
    ),
    path("register/", RegisterView.as_view(), name="register"),
]
