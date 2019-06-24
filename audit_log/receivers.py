from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from core.models import FavoriteThing, AuditLog


@receiver(post_save, sender=FavoriteThing)
def audit_handler_save(sender, **kwargs):
    title = kwargs.get('instance').title
    user = kwargs.get('instance').user
    message = f'favorite thing "{title}" was updated'
    if kwargs.get('created', True):
        message = f'favorite thing "{title}" was created'

    AuditLog.objects.create(log=message, user=user)


@receiver(post_delete, sender=FavoriteThing)
def audit_handler_delete(sender, **kwargs):
    title = kwargs.get('instance').title
    user = kwargs.get('instance').user
    message = f'favorite thing "{title}" was deleted'
    AuditLog.objects.create(log=message, user=user)
