from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    class UserRoles(models.TextChoices):
        BARBER = "B", "Barber"
        CLIENT = "C", "Client"

    phone_number = models.CharField(max_length=10, unique=True)
    role = models.CharField(
        max_length=1,
        choices=UserRoles.choices,
        default=UserRoles.CLIENT
    )

    def __str__(self):
        return f"{self.username}"


class BarberProfile(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )
    bio = models.TextField(null=True, blank=True)
    photo = models.ImageField(null=True, blank=True)
    is_active = models.BooleanField(default=True)


    def __str__(self):
        return f"{self.user}"


class ClientProfile(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )


    def __str__(self):
        return f"{self.user}"


class Service(models.Model):
    name = models.CharField(max_length=255, unique=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    duration_minutes = models.PositiveIntegerField()
    is_active = models.BooleanField(default=True)


    def __str__(self):
        return f"{self.name}"


class Schedule(models.Model):
    class Weekday(models.IntegerChoices):
        MONDAY = 0, "Monday"
        TUESDAY = 1, "Tuesday"
        WEDNESDAY = 2, "Wednesday"
        THURSDAY = 3, "Thursday"
        FRIDAY = 4, "Friday"
        SATURDAY = 5, "Saturday"
        SUNDAY = 6, "Sunday"


    barber = models.ForeignKey(
        BarberProfile,
        on_delete=models.CASCADE,
        related_name="schedules"
    )
    weekday = models.IntegerField(choices=Weekday.choices)
    start_time = models.TimeField()
    end_time = models.TimeField()


    def __str__(self):
        return (
            f"{self.barber.user.username}: "
            f"{self.weekday} weekday "
            f"(from {self.start_time} to {self.end_time})"
        )


class Booking(models.Model):
    class BookingStatus(models.TextChoices):
        CONFIRMED = "CF", "Confirmed"
        CANCELED = "CC", "Canceled"
        COMPLETED = "CP", "Completed"
        NO_SHOW = "NS", "No show"


    client = models.ForeignKey(
        ClientProfile,
        on_delete=models.CASCADE,
        related_name="bookings"
    )
    barber = models.ForeignKey(
        BarberProfile,
        on_delete=models.CASCADE,
        related_name="bookings"
    )
    service = models.ForeignKey(
        Service,
        on_delete=models.CASCADE,
        related_name="bookings"
    )
    start_at = models.DateTimeField()
    end_at = models.DateTimeField()
    status = models.CharField(
        max_length=2,
        choices=BookingStatus.choices,
        default=BookingStatus.CONFIRMED
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return (
            f"{self.client.user} to barber "
            f"{self.barber.user} on "
            f"{self.start_at.strftime('%A')} "
            f"at {self.start_at.time()}")