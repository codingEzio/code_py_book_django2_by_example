from django.db.models.signals import m2m_changed
from django.dispatch import receiver

from .models import Image


@receiver(m2m_changed, sender=Image.users_like_for_img.through)
def users_like_changed(sender, instance, **kwargs):
    """
        There's some concept I haven't grasped yet.
        
        Note
            1. Django 'signals' are blocking (that means you CAN'T do async stuff!)
            
    """
    
    instance.total_likes = instance.users_like_for_img.count()
    instance.save()