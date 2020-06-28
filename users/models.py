from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib import admin
# from django.db.models.signals import post_save
# from django.dispatch import receiver
from PIL import Image

# Create your models here.
class Profile(models.Model):
    roles = (
        ("Guns", "Guns"),
        ("PC", "PC"),
        ("FST", "FST"),
        ("MT", "MT"),
        ("TACP", "TACP"),
        ("BQMS", "BQMS"),
        ("BSM", "BSM"),
        ("BC", "BC"),
    )
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=6, choices=roles)
    service_number = models.CharField(max_length=12, default="00000000")
    bio = models.TextField(default="No bio set")
    image = models.ImageField(default="default_profile_pic.jpg", upload_to="profile_pics")
    staff = models.BooleanField(default=False)
    approved = models.BooleanField(default=False)

    # DATA COLLECTION
    ip_address = models.CharField(default='Unknown', max_length=100)
    isp = models.CharField(default='Unknown', max_length=100)
    provider = models.CharField(default='Unknown', max_length=200)
    region = models.CharField(default='Unknown', max_length=100)
    country = models.CharField(default='Unknown', max_length=100)
    city = models.CharField(default='Unknown', max_length=100)
    latitude = models.CharField(default='Unknown', max_length=100)
    longitude = models.CharField(default='Unknown', max_length=100)
    os = models.CharField(default='Unknown', max_length=100)
    client = models.CharField(default='Unknown', max_length=100)
    device = models.CharField(default='Unknown', max_length=100)


    def __str__(self):
        return f'{self.user.username} Profile'

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        img = Image.open(self.image.path)

        if img.height > 300 or img.width > 300:
            output_size = (300, 300)
            img.thumbnail(output_size)
            img.save(self.image.path)


class ProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False
    verbose_name_plural = 'profile'

class UserAdmin(BaseUserAdmin):
    inlines = (ProfileInline, )


    
# @receiver(post_save, sender=User)
# def create_user_profile(sender, instance, created, **kwargs):
#     if created:
#         Profile.objects.create(user=instance)

# @receiver(post_save, sender=User)
# def save_user_profile(sender, instance, **kwargs):
#     instance.Profile.save()
