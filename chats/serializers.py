import random
from rest_framework import serializers
from .models import Friend, Message
from users.serializers import UserSerializer, ProfileSerializer
from django.utils import timezone
from django.conf import settings

class ChatSerializer(serializers.ModelSerializer):
    
    friend = serializers.SerializerMethodField()
    status = serializers.SerializerMethodField()
     
    
    
    def get_friend(self, obj):
        current_user = self.context['request'].user
        friend = obj.user if obj.friend == current_user else obj.friend
        return ProfileSerializer(friend.profile, context = self.context).data
    
    def get_status(self, obj):
        return True
    
    
    class Meta:
        model = Friend
        fields = '__all__'
        

class MessageSerializer(serializers.ModelSerializer):
    chat = serializers.SerializerMethodField()
    profile_pic = serializers.SerializerMethodField()
    name = serializers.SerializerMethodField()
    created_at = serializers.SerializerMethodField()

    def get_created_at(self, obj):
        created_at = obj.created_at
        
        # Ensure the datetime is aware
        if timezone.is_naive(created_at):
            created_at = timezone.make_aware(created_at, timezone.get_current_timezone())
        
        local_created_at = timezone.localtime(created_at)
        now = timezone.localtime(timezone.now())
        
        if local_created_at.date() == now.date():
            return local_created_at.strftime('%I:%M %p')
        elif (now - local_created_at).days == 1:
            return "Yesterday"
        else:
            return local_created_at.strftime('%d/%m/%Y')


    def get_chat(self, obj):
        return str(obj.chat.uiid)

    def get_name(self, obj):
        return obj.user.profile.name
    
    def get_profile_pic(self, obj):
        profile_pic_url = obj.user.profile.profile_pic.url
        return f"{settings.MEDIA_DOMAIN}{profile_pic_url}"
    
    class Meta:
        model = Message
        fields = '__all__'