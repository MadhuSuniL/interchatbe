from django.db import models
from helper.models import Creation, UIID
from django.contrib.auth.models import User
from users.models import Profile

class Friend(Creation, UIID):
    user = models.ForeignKey(User, related_name='friends', on_delete=models.CASCADE)
    friend = models.ForeignKey(User, related_name='friend_of', on_delete=models.CASCADE)
    
    def __str__(self) -> str:
        return f"{self.user.username} <--> {self.friend.username}"
    
class Message(Creation, UIID):
    chat = models.ForeignKey(Friend, to_field='uiid', related_name = 'messages', on_delete=models.CASCADE)
    user = models.ForeignKey(User, related_name= 'messages', on_delete= models.CASCADE) 
    user_name = models.CharField(max_length=50, null = True, blank = True)
    message = models.TextField()


    def save(self, *args, **kwargs):
        if self.user:
            self.user_name = Profile.objects.get(user = self.user).name
        return super().save(*args, **kwargs)
    
    class Meta:
        ordering = ['created_at']