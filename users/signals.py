from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

from django.contrib.auth.models import User
from .models import Profile 

#@receiver(post_save, sender=Profile)
def createProfile(sender, instance, created, **kwargs):
   #check if its first instance 
   if created:
       user = instance
       # create a profile
       profile = Profile.objects.create(user=user, username = user.username, email = user.email, name=user.first_name)


def deleteUser(sender, instance, **kwargs):
    try:
        print("Deleting user...")
        user = instance.user
        user.delete()
    except User.DoesNotExist:
        print("User does not exist. This has to do with the relationship between User and Profile.")

  

post_save.connect(createProfile, sender=Profile)



post_delete.connect(deleteUser, sender=Profile)