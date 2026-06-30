from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.conf import settings

from .models import Profile


# CREATE PROFILE automatically after signup
@receiver(post_save, sender=User)
def createProfile(sender, instance, created, **kwargs):

    if created:

        profile = Profile.objects.create(
            user=instance,
            username=instance.username,
            email=instance.email,
            name=instance.first_name
        )

        print("Profile created:", profile)

        # Optional welcome email
        if profile.email:
            try:
                send_mail(
                    "Welcome to Soko Direct",
                    "We are glad you joined Soko Direct.",
                    settings.DEFAULT_FROM_EMAIL,
                    [profile.email],
                    fail_silently=True
                )
            except Exception:
                pass


# UPDATE USER when profile changes
@receiver(post_save, sender=Profile)
def updateUser(sender, instance, created, **kwargs):

    if not created:

        user = instance.user

        user.username = instance.username

        if instance.email:
            user.email = instance.email

        if instance.name:
            user.first_name = instance.name

        user.save()


# DELETE USER when profile deleted
@receiver(post_delete, sender=Profile)
def deleteUser(sender, instance, **kwargs):

    try:

        user = instance.user

        if user:
            user.delete()

    except:
        pass