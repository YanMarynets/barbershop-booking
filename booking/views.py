import datetime

from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views import generic, View
from formtools.wizard.views import SessionWizardView

from booking.forms import FirstStepBookingForm, SecondStepBookingForm, ThirdStepBookingForm, FourthStepBookingForm, \
    UserRegistrationForm
from booking.models import BarberProfile, Service, Booking
from booking.services import BookingService, InvalidBookingSlotError, SlotIsTakenError


class HomeView(generic.TemplateView):
    template_name = "booking/home.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context["barbers"] = BarberProfile.objects.filter(is_active=True)[:3]
        context["services"] = Service.objects.filter(is_active=True)[:3]

        return context




class BarberListView(generic.ListView):
    model = BarberProfile
    template_name = "booking/barber_list.html"
    context_object_name = "barbers"


class BarberDetailView(generic.DetailView):
    model = BarberProfile
    template_name = "booking/barber_detail.html"
    context_object_name = "barber"


class ServiceListView(generic.ListView):
    model = Service
    template_name = "booking/service_list.html"
    context_object_name = "services"


class BookingListView(LoginRequiredMixin, generic.ListView):
    model = Booking
    template_name = "booking/booking_list.html"

    def get_queryset(self):
        return Booking.objects.filter(client=self.request.user.client)


class BarberBookingListView(LoginRequiredMixin, UserPassesTestMixin, generic.ListView):
    model = Booking
    template_name = "booking/barber_booking_list.html"

    def get_queryset(self):
        return Booking.objects.filter(barber=self.request.user.barber).order_by("start_at")

    def test_func(self):
        return self.request.user.role == get_user_model().UserRoles.BARBER

class BookingCreateView(LoginRequiredMixin, SessionWizardView):
    template_name = "booking/booking_create.html"
    form_list = [
        ("barber", FirstStepBookingForm),
        ("service", SecondStepBookingForm),
        ("date", ThirdStepBookingForm),
        ("time", FourthStepBookingForm),
    ]


    def get_form_kwargs(self, step=''):
        kwargs = super().get_form_kwargs(step)

        if step == "date":
            barber_data = self.get_cleaned_data_for_step("barber")
            barber = barber_data["barber"]
            kwargs["barber"] = barber

        if step == "time":
            date_data = self.get_cleaned_data_for_step("date")
            barber_data = self.get_cleaned_data_for_step("barber")

            barber = barber_data["barber"]
            date = date_data["date"]

            kwargs["barber"], kwargs["date"] = barber, date

        return kwargs

    def done(self, form_list, **kwargs):
        all_cleaned_data = self.get_all_cleaned_data()

        date_data = all_cleaned_data["date"]
        time_data = all_cleaned_data["time"]

        time_data = datetime.datetime.strptime(
            time_data,"%H:%M"
        ).time()

        start_at = datetime.datetime.combine(date_data, time_data)
        barber = all_cleaned_data["barber"]
        service = all_cleaned_data["service"]

        try:
            BookingService.create_booking(
                client=self.request.user.client,
                barber=barber,
                start_at=start_at,
                service=service
            )
            return redirect("booking:booking-list")
        except InvalidBookingSlotError:
            messages.error(
                self.request,
                "This is invalid time slot"
            )
        except SlotIsTakenError:
            messages.error(
                self.request,
                "This time slot is already taken"
            )
        return self.render_goto_step("time")


class RegisterView(generic.CreateView):
    form_class = UserRegistrationForm
    template_name = "registration/register.html"
    success_url = reverse_lazy("login")


class BookingCancellationView(LoginRequiredMixin, View):
    def post(self, request, pk):
        booking = Booking.objects.get(
            pk=pk,
            client=request.user.client
        )
        booking.status = Booking.BookingStatus.CANCELED
        booking.save()

        return redirect("booking:booking-list")


class BookingStatusUpdateView(LoginRequiredMixin, UserPassesTestMixin, View):
    def post(self, request, pk):
        booking = Booking.objects.get(
            pk=pk,
            barber=request.user.barber
        )
        status = request.POST["status"]
        booking.status = status
        booking.save()
        return  redirect("booking:barber-booking-list")

    def test_func(self):
        return self.request.user.role == get_user_model().UserRoles.BARBER