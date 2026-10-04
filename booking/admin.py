from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin

from booking.models import Schedule, ClientProfile

User = get_user_model()

@admin.register(Schedule)
class ProductAdmin(admin.ModelAdmin):
   list_display = ("barber", "weekday", "start_time", "end_time")


@admin.register(ClientProfile)
class ProductAdmin(admin.ModelAdmin):
   pass


@admin.register(User)
class ProductAdmin(UserAdmin):
   pass

