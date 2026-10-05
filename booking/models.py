from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
from django.db import models


phone_validator = RegexValidator(
    regex=r"^0\d{9}$",
    message="Phone number must contain exactly 10 digits.",
)


class User(AbstractUser):
    class UserRoles(models.TextChoices):
        BARBER = "B", "Barber"
        CLIENT = "C", "Client"

    phone_number = models.CharField(
        max_length=10, unique=True, validators=[phone_validator]
    )
    role = models.CharField(
        max_length=1, choices=UserRoles.choices, default=UserRoles.CLIENT
    )

    def __str__(self):
        return f"{self.username}"


class BarberProfile(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="barber",
    )
    bio = models.TextField(null=True, blank=True)
    photo = models.ImageField(upload_to="barbers/", blank=True, null=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.user}"


class ClientProfile(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="client",
    )

    def __str__(self):
        return f"{self.user}"


class Service(models.Model):
    name = models.CharField(max_length=255, unique=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    duration_minutes = models.PositiveIntegerField(default=60)
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
        BarberProfile, on_delete=models.CASCADE, related_name="schedules"
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
        ClientProfile, on_delete=models.CASCADE, related_name="bookings"
    )
    barber = models.ForeignKey(
        BarberProfile, on_delete=models.CASCADE, related_name="bookings"
    )
    service = models.ForeignKey(
        Service, on_delete=models.CASCADE, related_name="bookings"
    )
    start_at = models.DateTimeField()
    end_at = models.DateTimeField()
    status = models.CharField(
        max_length=2,
        choices=BookingStatus.choices,
        default=BookingStatus.CONFIRMED,
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return (
            f"{self.client.user} to barber "
            f"{self.barber.user} on "
            f"{self.start_at.strftime('%A')} "
            f"at {self.start_at.time()}"
        )
