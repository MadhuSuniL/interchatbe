import random
from rest_framework import serializers
from .models import Friend, Message
from users.serializers import UserSerializer, ProfileSerializer
from django.contrib.humanize.templatetags.humanize import naturaltime

class ChatSerializer(serializers.ModelSerializer):
    
    user = serializers.SerializerMethodField()
    friend = serializers.SerializerMethodField()
    status = serializers.SerializerMethodField()
    # last_message = serializers.SerializerMethodField()
     
    
    def get_user(self, obj):
        return ProfileSerializer(obj.user.profile, context = self.context).data

    def get_friend(self, obj):
        return ProfileSerializer(obj.friend.profile, context = self.context).data
    
    def get_status(self, obj):
        return random.choice([True, False])
    
    # def get_last_message(self, obj):
    #     return {
    #             'message' : 'Nope',
    #             'is_self_message' : True
    #     }

    
    class Meta:
        model = Friend
        fields = '__all__'
        

class MessageSerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField()
    created_at = serializers.SerializerMethodField()

    def get_created_at(self, obj):
        return naturaltime(obj.created_at)

    def get_name(self, obj):
        return self.obj.profile.name

    
    class Meta:
        model = Message
        fields = '__all__'