from rest_framework import serializers
from .models import FriendRequest
from users.serializers import UserSerializer

class FriendRequestSerializer(serializers.ModelSerializer):
    from_user = UserSerializer()
    to_user = UserSerializer()
    
    class Meta:
        model = FriendRequest
        fields = '__all__'
        