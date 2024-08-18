# myapp/signals.py

from django.db.models.signals import post_save, post_delete
from django.db.models import Q
from django.dispatch import receiver
from helper.choices import SUCCESS
from chats.models import Friend
from .models import FriendRequest

@receiver(post_save, sender=FriendRequest)
def add_friend(sender, instance, created, **kwargs):
    if not created and instance.status == SUCCESS:
        from_user = instance.from_user
        to_user = instance.to_user
        Friend.objects.get_or_create(user = from_user, friend = to_user)
        
        
@receiver(post_delete, sender=FriendRequest)
def remove_friend(sender, instance, **kwargs):
    from_user = instance.from_user
    to_user = instance.to_user
    try:
        Friend.objects.get(Q(user = from_user, friend = to_user) | Q(user = to_user, friend = from_user)).delete()
    except Friend.DoesNotExist:
        pass
        
