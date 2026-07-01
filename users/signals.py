# users/signals.py (new file)

from django.db.models.signals import post_save, post_delete

# using django decorators to connect the receiver function to the signal
from django.dispatch import receiver

from django.contrib.auth.models import User # Django's built-in User model
from .models import Profile # import the Profile model to create a profile when a user is created

from django.core.mail import send_mail
from django.conf import settings

# this is the receiver function (profileUpdated)
# that we are going to trigger when a new user is created
# where we will parse some sender 
# the sender is the model (User) that sends this signal and 
# the instance is the actual user that was created
#@receiver(post_save, sender=User) # this is a decorator that connects the receiver function to the post_save signal of the User model
def CreateProfile(sender, instance, created, **kwargs):
    print('Profile signal triggered!!')
    if created: # only create profile if user is created, not updated
        user = instance # the user that was created
        profile = Profile.objects.create( # create a new profile with the following fields
            user=user, # link the profile to the user
            username=user.username, # copy username from user to profile for easy access
            email=user.email, # copy email from user to profile for easy access
            name=user.first_name # copy first name from user to profile for easy access
        )
        #print('Profile created for user: ', profile)

        subject = 'Welcome to SokoDirect'
        message = 'We are glad you are here!!'

        send_mail(
            subject,
            message,
            settings.EMAIL_HOST_USER,
            [profile.email],
            fail_silently=False,
        )

def updateUser(sender, instance, created, **kwargs):
    profile = instance 
    user = profile.user 
    
    if created == False: 
        user.username = profile.username
        user.email = profile.email 
        user.first_name = profile.name 
        user.save() 

def deleteUser(sender, instance, **kwargs):
    try:
        user = instance.user
        if user:
            user.delete()
            print('🗑️ SokoDirect Signal: Associated auth credentials safely pruned.')
    except Exception:
        # If the User was deleted first, the profile is cascade-deleted, 
        # and instance.user will throw an error. We catch it here to prevent crashes.
        print('💡 SokoDirect Signal: User was already deleted. Profile cascade complete.')

# Every time a user is created, 
# the CreateProfile function will be called to create a corresponding profile

post_save.connect(CreateProfile, sender=User)    


post_save.connect(updateUser, sender=Profile) 

# When a profile is deleted 
# we want to delete the corresponding user as well, 
# from the User model
post_delete.connect(deleteUser, sender=Profile) 
