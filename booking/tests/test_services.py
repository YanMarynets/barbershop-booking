import datetime

from django.contrib.auth import get_user_model
from django.test import TestCase

from booking.models import (
    BarberProfile,
    Booking,
    ClientProfile,
    Schedule,
    Service,
)
from booking.services import (
    BookingService,
    InvalidBookingSlotError,
    SlotIsTakenError,
)


class TestBookingService(TestCase):
    def setUp(self):
        self.user_barber = get_user_model().objects.create_user(
            username="test_user",
            password="1234testpass",
            first_name="Jack",
            last_name="Black",
            phone_number="0671234567",
            role=get_user_model().UserRoles.BARBER,
        )

        self.user_client = get_user_model().objects.create_user(
            username="test_user2",
            password="1234mysecRetpass",
            first_name="Bob",
            last_name="Jackson",
            phone_number="0677654321",
        )

        self.barber = BarberProfile.objects.create(user=self.user_barber)
        self.client_profile = ClientProfile.objects.create(
            user=self.user_client
        )

        self.service = Service.objects.create(
            name="Haircut",
            price=20.00,
            duration_minutes=60,
        )

        self.schedule = Schedule.objects.create(
            barber=self.barber,
            weekday=Schedule.Weekday.MONDAY,
            start_time=datetime.time(9, 0),
            end_time=datetime.time(17, 0),
        )

    # create_booking

    def test_create_booking(self):
        start_at = datetime.datetime(2026, 1, 5, 10, 0)

        booking = BookingService.create_booking(
            barber=self.barber,
            service=self.service,
            start_at=start_at,
            client=self.client_profile,
        )

        self.assertEqual(Booking.objects.count(), 1)
        self.assertEqual(booking.client, self.client_profile)
        self.assertEqual(booking.barber, self.barber)

    def test_create_booking_for_invalid_slot(self):
        start_at = datetime.datetime(2026, 1, 5, 10, 30)

        with self.assertRaises(InvalidBookingSlotError):
            BookingService.create_booking(
                barber=self.barber,
                service=self.service,
                start_at=start_at,
                client=self.client_profile,
            )

    def test_create_booking_for_taken_slot(self):
        start_at = datetime.datetime(2026, 1, 5, 10, 0)

        BookingService.create_booking(
            barber=self.barber,
            service=self.service,
            start_at=start_at,
            client=self.client_profile,
        )

        with self.assertRaises(SlotIsTakenError):
            BookingService.create_booking(
                barber=self.barber,
                service=self.service,
                start_at=start_at,
                client=self.client_profile,
            )

    # generate_booking_slots

    def test_generate_booking_slots(self):
        date = datetime.date(2026, 1, 5)

        slots = BookingService.generate_booking_slots(
            barber=self.barber,
            date=date,
        )

        expected_slots = [
            datetime.datetime(2026, 1, 5, 9, 0),
            datetime.datetime(2026, 1, 5, 10, 0),
            datetime.datetime(2026, 1, 5, 11, 0),
            datetime.datetime(2026, 1, 5, 12, 0),
            datetime.datetime(2026, 1, 5, 13, 0),
            datetime.datetime(2026, 1, 5, 14, 0),
            datetime.datetime(2026, 1, 5, 15, 0),
            datetime.datetime(2026, 1, 5, 16, 0),
        ]

        self.assertEqual(slots, expected_slots)

    def test_generate_booking_slots_for_day_off(self):
        date = datetime.date(2026, 1, 6)

        slots = BookingService.generate_booking_slots(
            barber=self.barber,
            date=date,
        )

        self.assertEqual(slots, [])
