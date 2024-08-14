from django.db import models
from helper.models import Creation, UIID
from django.contrib.auth.models import User
from helper.choices import REQUEST_STATUS_CHOICES, PENDING

class FriendRequest(UIID, Creation):
    
    from_user = models.ForeignKey(User, related_name='sent_requests', on_delete=models.CASCADE)
    to_user = models.ForeignKey(User, related_name='received_requests', on_delete=models.CASCADE)
    status = models.CharField(max_length=10, choices=REQUEST_STATUS_CHOICES, default=PENDING)
    
    def __str__(self):
        return f"{self.from_user.username} sent a request to {self.to_user.username}"

