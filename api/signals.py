import logging

from django.db.models.signals import post_delete, post_save
from django.dispatch import receiver

from .models import Book

logger = logging.getLogger(__name__)


@receiver(post_save, sender=Book)
def book_create_or_update_handler(sender, instance, created, **kwargs):
    action = "created" if created else "updated"
    logger.info(
        f"{sender.__name__}_{instance.id} {action}. Attributes: {instance.__dict__}"
    )


@receiver(post_delete, sender=Book)
def book_delete_handler(sender, instance, **kwargs):
    logger.info(f"{sender.__name__}_{instance.id} deleted")
