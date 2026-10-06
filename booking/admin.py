from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin

from booking.models import (
    Schedule,
    ClientProfile,
    BarberProfile,
    Booking,
    Service,
)


User = get_user_model()


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = UserAdmin.list_display + (
        "phone_number",
        "role",
        "is_active",
    )
    list_filter = ("role", "is_active", "is_staff")

    search_fields = UserAdmin.search_fields + ("phone_number", "role")

    fieldsets = UserAdmin.fieldsets + (
        (
            "Additional info",
            {
                "fields": (
                    "phone_number",
                    "role",
                )
            },
        ),
    )

    add_fieldsets = UserAdmin.add_fieldsets + (
        (
            "Additional info",
            {
                "fields": (
                    "phone_number",
                    "role",
                )
            },
        ),
    )


@admin.register(ClientProfile)
class ClientProfileAdmin(admin.ModelAdmin):
    list_display = ("user",)
    search_fields = (
        "user__username",
        "user__first_name",
        "user__last_name",
        "user__email",
    )


@admin.register(BarberProfile)
class BarberProfileAdmin(admin.ModelAdmin):
    list_display = ("user", "is_active")
    list_filter = ("is_active",)
    search_fields = (
        "user__username",
        "user__first_name",
        "user__last_name",
    )


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "price",
        "duration_minutes",
        "is_active",
    )
    list_filter = ("is_active",)
    search_fields = ("name",)


@admin.register(Schedule)
class ScheduleAdmin(admin.ModelAdmin):
    list_display = ("barber", "weekday", "start_time", "end_time")
    list_filter = ("weekday", "barber")


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = (
        "client",
        "barber",
        "service",
        "start_at",
        "status",
        "created_at",
    )
    list_filter = (
        "status",
        "barber",
        "service",
    )
    search_fields = (
        "client__user__username",
        "client__user__first_name",
        "client__user__last_name",
        "barber__user__username",
        "service__name",
    )
    ordering = ("-start_at",)
    readonly_fields = ("created_at",)
