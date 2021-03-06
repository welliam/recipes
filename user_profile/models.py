from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver


class UserProfile(models.Model):
    """Extended user information."""

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name="profile",
    )
    bio = models.TextField(max_length=1000, blank=True)
    follows = models.ManyToManyField(
        User,
        related_name="followers"
    )

    def __str__(self):
        return "{}'s profile".format(self.user.username)


@receiver(post_save, sender=User)
def update_tracker_profile(sender, **kwargs):
    if not UserProfile.objects.filter(user=kwargs['instance']):
        UserProfile(user=kwargs['instance']).save()
