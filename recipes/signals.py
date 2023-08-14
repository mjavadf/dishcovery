from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings
from .models import Profile

@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_profle_for_new_user(sender, created, instance, **kwargs):
    if created:
        Profile.objects.create(user=instance)
