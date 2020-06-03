from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from users.models import Details

# Register your models here.
class DetailsInline(admin.StackedInline):
    model = Details
    can_delete = False
    verbose_name_plural = 'details'

class UserAdmin(BaseUserAdmin):
    inlines = (DetailsInline, )

# Re-register UserAdmin
admin.site.unregister(User)
admin.site.register(User, UserAdmin)