import datetime

from django.contrib.auth import get_user_model
from django.db import transaction

from booking.models import Booking, Schedule, ClientProfile


class BookingSlotError(Exception):
    pass


class SlotIsTakenError(BookingSlotError):
    pass


class InvalidBookingSlotError(BookingSlotError):
    pass


class BookingService:
    @classmethod
    def create_booking(cls, barber, service, start_at, client):
        end_at = cls.get_end_at(
            start_at=start_at,
            service=service,
        )

        if start_at not in cls.generate_booking_slots(
            barber,
            start_at.date(),
        ):
            raise InvalidBookingSlotError

        if not cls.check_booking_time(
            start_at=start_at,
            barber=barber,
        ):
            raise SlotIsTakenError

        return Booking.objects.create(
            barber=barber,
            client=client,
            service=service,
            start_at=start_at,
            end_at=end_at,
        )

    @staticmethod
    def get_end_at(start_at, service):
        return start_at + datetime.timedelta(minutes=service.duration_minutes)

    @staticmethod
    def check_booking_time(start_at, barber):
        return not barber.bookings.filter(
            start_at=start_at,
            status="CF",
        ).exists()

    @staticmethod
    def generate_booking_slots(barber, date):
        try:
            schedule = barber.schedules.get(weekday=date.weekday())
        except Schedule.DoesNotExist:
            return []

        start_datetime = datetime.datetime.combine(
            date,
            schedule.start_time,
        )
        end_datetime = datetime.datetime.combine(
            date,
            schedule.end_time,
        )

        slots = []
        current_time = start_datetime

        while current_time < end_datetime:
            slots.append(current_time)
            current_time += datetime.timedelta(hours=1)

        return slots

    def get_available_slots(self, barber, date):
        all_slots = self.generate_booking_slots(barber, date)
        return [
            slot for slot in all_slots if self.check_booking_time(slot, barber)
        ]

    @staticmethod
    def get_available_dates():
        today = datetime.date.today()

        return [today + datetime.timedelta(days=days) for days in range(1, 15)]

    def get_barber_available_dates(self, barber):
        dates = self.get_available_dates()
        working_days = barber.schedules.values_list("weekday", flat=True)
        print("DATES:", dates)
        print("WORKING DAYS:", list(working_days))
        return [date for date in dates if date.weekday() in working_days]


class UserService:
    User = get_user_model()

    def create_client(
        self, username, email, password, first_name, last_name, phone_number
    ):
        with transaction.atomic():
            user = self.User.objects.create_user(
                username=username,
                email=email,
                password=password,
                first_name=first_name,
                last_name=last_name,
                phone_number=phone_number,
            )
            ClientProfile.objects.create(user=user)
            return user
