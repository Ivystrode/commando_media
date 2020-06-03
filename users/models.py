from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

# Create your models here.
class Details(models.Model):
    roles = (
        ("Guns", "Guns"),
        ("FST", "FST"),
        ("MT", "MT"),
        ("TACP", "TACP"),
        ("BQMS", "BQMS"),
        ("BSM", "BSM"),
        ("BC", "BC"),
    )
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=6, choices=roles)

# @receiver(post_save, sender=User)
# def create_user_profile(sender, instance, created, **kwargs):
#     if created:
#         Details.objects.create(user=instance)

# @receiver(post_save, sender=User)
# def save_user_profile(sender, instance, **kwargs):
#     instance.details.save()