from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from users.models import Profile

# Register your models here.
# class ProfileInline(admin.StackedInline):
#     model = Profile
#     can_delete = False
#     verbose_name_plural = 'profile'

# class UserAdmin(BaseUserAdmin):
#     inlines = (ProfileInline, )

# # Re-register UserAdmin
# admin.site.unregister(User)
# admin.site.register(User, UserAdmin)

# ^^^ makes the "profile" details appear on the main user page of admin panel

admin.site.register(Profile)