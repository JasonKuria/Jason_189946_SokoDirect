from django.db import models
from django.contrib.auth.models import User
import uuid


class Profile(models.Model):

    ROLE_CHOICES = [
        ('buyer', 'Buyer'),
        ('farmer', 'Farmer'),
    ]

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE
    )

    role = models.CharField(
        max_length=10,
        choices=ROLE_CHOICES
    )

    username = models.CharField(
        max_length=200,
        blank=True,
        null=True
    )

    email = models.EmailField(
        blank=True,
        null=True
    )

    bio = models.TextField(
        blank=True,
        null=True
    )

    created = models.DateTimeField(
        auto_now_add=True
    )

    id = models.UUIDField(
        default=uuid.uuid4,
        primary_key=True,
        editable=False
    )

    def __str__(self):
        return f'{self.user.username} - {self.role}'


class Speciality(models.Model):

    owner = models.ForeignKey(
        Profile,
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )

    name = models.CharField(
        max_length=200
    )

    description = models.TextField(
        blank=True,
        null=True
    )

    def __str__(self):
        return self.name


class Message(models.Model):

    sender = models.ForeignKey(
        Profile,
        on_delete=models.SET_NULL,
        null=True
    )

    subject = models.CharField(
        max_length=200
    )

    body = models.TextField()

    is_read = models.BooleanField(
        default=False
    )

    def __str__(self):
        return self.subject