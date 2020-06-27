from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from users.models import *

# Register your models here.


# Re-register UserAdmin
admin.site.unregister(User)
admin.site.register(User, UserAdmin)

# ^^^ makes the "profile" details appear on the main user page of admin panel