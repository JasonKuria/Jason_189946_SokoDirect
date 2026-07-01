from django.contrib import admin

# Register your models here.
from .models import Profile, Speciality, Message

# Register so they appear in the admin panel
admin.site.register(Profile)
admin.site.register(Speciality)
admin.site.register(Message)

