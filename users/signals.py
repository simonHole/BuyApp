from django.contrib.auth.models import User
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

from .models import *
from django.conf import settings


@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        user = instance
        profile = Profile.objects.create(
            user=user,
            nickname=user.username,
            email=user.email,
            full_name=user.last_name + ' ' + user.first_name,
        )

        print(f'create_profile {profile.nickname} successfully created')


@receiver(post_save, sender=Profile)
def update_user(sender, instance, created, **kwargs):
    profile = instance
    user = profile.user

    if created == False:
        full_name = profile.full_name.split()
        if len(full_name) == 1:
            user.first_name = full_name[0]
            user.last_name = ''
        else:
            user.first_name = full_name[0]
            user.last_name = full_name[1]
        user.username = profile.nickname
        user.email = profile.email
        user.save()


@receiver(post_delete, sender=User)
def delete_profile(sender, instance, **kwargs):
    profile = instance.profile
    if profile:
        profile.delete()
        print(f'delete_profile: {instance.username} successfully deleted')
    else:
        pass
