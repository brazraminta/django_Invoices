from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import UserAction

@receiver(post_save, sender=UserAction)
def log_user_action(sender, instance, created, **kwargs):
    if created:
        action = "Action created"
    else:
        action = "Action updated"
    UserAction.objects.create(user=instance.user, action=action)

