from rest_framework import serializers
from .models import FriendRequest
from users.serializers import UserSerializer, ProfileSerializer
from django.contrib.humanize.templatetags.humanize import naturaltime

class FriendRequestSerializer(serializers.ModelSerializer):
    from_user = serializers.SerializerMethodField()
    to_user = serializers.SerializerMethodField()
    created_at = serializers.SerializerMethodField()
    
    def get_from_user(self, obj):
        return ProfileSerializer(obj.from_user.profile, context = self.context).data

    def get_to_user(self, obj):
        return ProfileSerializer(obj.to_user.profile, context = self.context).data

    def get_created_at(self, obj):
        return naturaltime(obj.created_at)

    class Meta:
        model = FriendRequest
        fields = '__all__'

