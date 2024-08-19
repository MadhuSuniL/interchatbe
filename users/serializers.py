from django.contrib.auth.models import User
from django.db.models import Q
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import serializers
from .models import Profile
from chats.models import Friend
from requests.models import FriendRequest


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        username = data.get("username")
        password = data.get("password")

        if username and password:
            user = authenticate(username=username, password=password)

            if user is None:
                raise serializers.ValidationError("Invalid credentials.")

            if not user.is_active:
                raise serializers.ValidationError("User is inactive.")

            data['user'] = user
        else:
            raise serializers.ValidationError("Must include 'username' and 'password'.")
        # self.validated_data = data
        return data
    

    def get_tokens_data(self):
        user = self.validated_data['user']
        refresh = RefreshToken.for_user(user)
        profile = Profile.objects.get(user = user)
        profile_data = ProfileSerializer(profile, context = self.context).data
        return {
            'refresh': str(refresh),
            'access': str(refresh.access_token),
            'user_id': user.id,
            'username': user.username,
        }.update(profile_data)
 

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ('username', 'password')

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            password=validated_data['password']
        )
        return user

class UserSerializer(serializers.ModelSerializer):
    

    class Meta:
        model = User
        fields = ['id', 'username']

    def update(self, instance, validated_data):
        # Extract nested profile data
        profile_data = validated_data.pop('profile', {})
        
        # Update user fields
        instance.username = validated_data.get('username', instance.username)
        instance.email = validated_data.get('email', instance.email)
        instance.save()

        # Update or create profile
        profile, created = Profile.objects.get_or_create(user=instance)
        profile.bio = profile_data.get('bio', profile.bio)
        if 'profile_pic' in profile_data:
            profile.profile_pic = profile_data['profile_pic']
        profile.save()

        return instance
    

class ProfileSerializer(serializers.ModelSerializer):
    is_friend = serializers.SerializerMethodField()
    is_requested = serializers.SerializerMethodField()
    total_friends = serializers.SerializerMethodField()
    user = UserSerializer()

    def get_is_friend(self, obj):
        try:
            request = self.context['request']
            current_user = request.user
        except KeyError :
            current_user = self.context['user']
            

        if current_user.is_anonymous:
            return None

        return current_user.friends.filter(Q(user=obj.user) | Q(friend = obj.user)).exists() or current_user.friend_of.filter(Q(user=obj.user) | Q(friend = obj.user)).exists() 

    def get_is_requested(self, obj):
        try:
            request = self.context['request']
            current_user = request.user
        except KeyError :
            current_user = self.context['user']


        if current_user.is_anonymous:
            return None

        return FriendRequest.objects.filter(from_user=current_user, to_user=obj.user).exists()

    def get_total_friends(self, obj):
        user = obj.user
        return Friend.objects.filter(Q(user = user) | Q(friend = user)).count()
        

    class Meta:
        model = Profile
        fields = ['name', 'bio', 'profile_pic', 'is_friend', 'is_requested', 'user', 'total_friends']
    
