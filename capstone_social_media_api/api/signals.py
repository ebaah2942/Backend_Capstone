from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Like, Comment, Notification

@receiver(post_save, sender=Like)
def create_like_notification(sender, instance, created, **kwargs):
    if created:
        Notification.objects.create(
            recipient=instance.post.user,
            sender=instance.user,
            type='like',
            post=instance.post
        )

@receiver(post_save, sender=Comment)
def create_comment_notification(sender, instance, created, **kwargs):
    if created:
        Notification.objects.create(
            recipient=instance.post.user,
            sender=instance.user,
            type='comment',
            post=instance.post
        )


