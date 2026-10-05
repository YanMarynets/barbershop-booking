import datetime

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from booking.models import (
    Booking,
    BarberProfile,
    ClientProfile,
    Service,
)


class BookingViewTestCase(TestCase):
    def setUp(self):
        self.user_client = get_user_model().objects.create_user(
            username="client",
            password="testpass123",
            phone_number="0671234567",
        )

        self.barber_user = get_user_model().objects.create_user(
            username="barber",
            password="testpass123",
            phone_number="0671111111",
            role=get_user_model().UserRoles.BARBER,
        )

        self.client_profile = ClientProfile.objects.create(
            user=self.user_client
        )

        self.barber = BarberProfile.objects.create(user=self.barber_user)

        self.service = Service.objects.create(
            name="Haircut",
            price=20,
            duration_minutes=60,
        )


class TestBookingListView(BookingViewTestCase):
    def setUp(self):
        super().setUp()

        self.other_user = get_user_model().objects.create_user(
            username="other_client",
            password="testpass123",
            phone_number="0677654321",
        )

        self.other_client_profile = ClientProfile.objects.create(
            user=self.other_user
        )

        self.other_service = Service.objects.create(
            name="Beard trim",
            price=15,
            duration_minutes=60,
        )

    def test_booking_list_requires_login(self):
        response = self.client.get(reverse("booking:booking-list"))

        self.assertEqual(response.status_code, 302)

    def test_booking_list_shows_only_current_users_bookings(self):
        self.client.force_login(self.user_client)

        Booking.objects.create(
            client=self.client_profile,
            barber=self.barber,
            service=self.service,
            start_at=datetime.datetime(2026, 10, 6, 10, 0),
            end_at=datetime.datetime(2026, 10, 6, 11, 0),
            status=Booking.BookingStatus.CONFIRMED,
        )

        Booking.objects.create(
            client=self.other_client_profile,
            barber=self.barber,
            service=self.other_service,
            start_at=datetime.datetime(2026, 10, 6, 11, 0),
            end_at=datetime.datetime(2026, 10, 6, 12, 0),
            status=Booking.BookingStatus.CONFIRMED,
        )

        response = self.client.get(reverse("booking:booking-list"))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Haircut")
        self.assertNotContains(response, "Beard trim")


class TestBarberBookingListView(BookingViewTestCase):
    def setUp(self):
        super().setUp()

        self.other_barber_user = get_user_model().objects.create_user(
            username="other_barber",
            password="testpass123",
            phone_number="0677654321",
            role=get_user_model().UserRoles.BARBER,
        )

        self.other_barber = BarberProfile.objects.create(
            user=self.other_barber_user
        )

    def test_barber_booking_list_requires_barber(self):
        self.client.force_login(self.user_client)

        response = self.client.get(reverse("booking:barber-booking-list"))

        self.assertEqual(response.status_code, 403)

    def test_barber_booking_list_shows_only_own_bookings(self):
        self.client.force_login(self.barber_user)

        my_booking = Booking.objects.create(
            client=self.client_profile,
            barber=self.barber,
            service=self.service,
            start_at=datetime.datetime(2026, 10, 6, 10, 0),
            end_at=datetime.datetime(2026, 10, 6, 11, 0),
            status=Booking.BookingStatus.CONFIRMED,
        )

        Booking.objects.create(
            client=self.client_profile,
            barber=self.other_barber,
            service=self.service,
            start_at=datetime.datetime(2026, 10, 6, 11, 0),
            end_at=datetime.datetime(2026, 10, 6, 12, 0),
            status=Booking.BookingStatus.CONFIRMED,
        )

        response = self.client.get(reverse("booking:barber-booking-list"))

        self.assertEqual(response.status_code, 200)

        bookings = response.context["booking_list"]

        self.assertIn(my_booking, bookings)
        self.assertEqual(bookings.count(), 1)


class TestBookingCancellationView(BookingViewTestCase):
    def test_client_can_cancel_own_booking(self):
        booking = Booking.objects.create(
            client=self.client_profile,
            barber=self.barber,
            service=self.service,
            start_at=datetime.datetime(2026, 10, 6, 10, 0),
            end_at=datetime.datetime(2026, 10, 6, 11, 0),
        )

        self.client.force_login(self.user_client)

        response = self.client.post(
            reverse("booking:booking-cancel", args=[booking.pk])
        )

        booking.refresh_from_db()

        self.assertEqual(response.status_code, 302)
        self.assertEqual(
            booking.status,
            Booking.BookingStatus.CANCELED,
        )


class TestBookingStatusUpdateView(BookingViewTestCase):
    def test_barber_can_update_booking_status(self):
        booking = Booking.objects.create(
            client=self.client_profile,
            barber=self.barber,
            service=self.service,
            start_at=datetime.datetime(2026, 10, 6, 10, 0),
            end_at=datetime.datetime(2026, 10, 6, 11, 0),
        )

        self.client.force_login(self.barber_user)

        response = self.client.post(
            reverse("booking:booking-update-status", args=[booking.pk]),
            {"status": Booking.BookingStatus.COMPLETED},
        )

        booking.refresh_from_db()

        self.assertEqual(response.status_code, 302)
        self.assertEqual(
            booking.status,
            Booking.BookingStatus.COMPLETED,
        )
