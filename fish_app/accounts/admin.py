from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import get_user_model
from accounts.forms import SignupForm

from .models import Connection, CustomUser, Message, Room

CustomUser = get_user_model()

class CustomUserAdmin(UserAdmin):
    add_form = SignupForm
    model = CustomUser
    list_display = ['email', 'username',]

admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Connection)
admin.site.register(Room)
admin.site.register(Message)