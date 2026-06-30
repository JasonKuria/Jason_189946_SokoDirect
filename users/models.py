
# Create your models here.
# users/models.py - MINIMAL version for now, expanded fully in Module 5
import uuid
from django.db import models
from django.contrib.auth.models import User
 
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE,
                                null=True, blank=True)
    name = models.CharField(max_length=200, null=True, blank=True)
    username = models.CharField(max_length=200, null=True, blank=True)
    id = models.UUIDField(default=uuid.uuid4, unique=True,
                          primary_key=True, editable=False)
    created = models.DateTimeField(auto_now_add=True)
 
    def __str__(self):
        return str(self.username)
