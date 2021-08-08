from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import Profile

# ? signals help give alert or perform specific actions when certain things(other actions happen)
@receiver(post_save, sender=User)
def createProfile(sender, instance, created, **kwargs):
    print("profile signal created! ")
    if created:
        user = instance
        profile = Profile.objects.create(
            user = user,
            username = user.username,
            email = user.email,
            name = user.first_name,
        ) 

@receiver(post_save, sender=Profile)
def updateUser(sender, instance, created, **kwkwargs):

    profile = instance
    user = profile.user
    if created == False:
        user.first_name = profile.name
        user.username = profile.username
        user.email = profile.email


@receiver(post_delete, sender=Profile)
def deleteUser(sender, instance, **kwargs):
    user = instance.user
    user.delete()




