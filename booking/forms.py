import datetime

from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm

from booking import services
from booking.models import BarberProfile, Service


class FirstStepBookingForm(forms.Form):
    barber = forms.ModelChoiceField(
        queryset=BarberProfile.objects.filter(is_active=True)
    )


class SecondStepBookingForm(forms.Form):
    service = forms.ModelChoiceField(
        queryset=Service.objects.filter(is_active=True)
    )


class ThirdStepBookingForm(forms.Form):
    date = forms.ChoiceField(choices=[])

    def __init__(self, *arg, **kwargs):
        barber = kwargs.pop("barber")
        super().__init__(*arg, **kwargs)
        booking_service = services.BookingService()
        dates = booking_service.get_barber_available_dates(barber)
        formatted_choices = [
            (date.strftime("%Y-%m-%d"), date.strftime("%d.%m.%Y"))
            for date in dates
        ]
        self.fields["date"].choices = formatted_choices

    def clean_date(self):
        date = self.cleaned_data.get("date")
        return datetime.datetime.strptime(date, "%Y-%m-%d").date()


class FourthStepBookingForm(forms.Form):
    time = forms.ChoiceField(choices=[])

    def __init__(self, *args, **kwargs):
        barber = kwargs.pop("barber")
        date = kwargs.pop("date")
        super().__init__(*args, **kwargs)
        booking_service = services.BookingService()
        slots = booking_service.get_available_slots(barber=barber, date=date)
        formatted_choices = [
            (slot.strftime("%H:%M"), slot.strftime("%H:%M")) for slot in slots
        ]
        self.fields["time"].choices = formatted_choices


class UserRegistrationForm(UserCreationForm):
    class Meta:
        model = get_user_model()
        fields = (
            "username",
            "first_name",
            "last_name",
            "email",
            "phone_number",
        )

    def save(self, commit=True):

        username = self.cleaned_data["username"]
        first_name = self.cleaned_data["first_name"]
        last_name = self.cleaned_data["last_name"]
        email = self.cleaned_data["email"]
        phone_number = self.cleaned_data["phone_number"]
        password = self.cleaned_data["password1"]

        client_create = services.UserService()
        return client_create.create_client(
            username=username,
            first_name=first_name,
            last_name=last_name,
            email=email,
            phone_number=phone_number,
            password=password,
        )
