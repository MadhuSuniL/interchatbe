from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import serializers
from .models import Profile


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

    

class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ['name', 'bio', 'profile_pic']

    # def create(self, validated_data):
    #     profile = Profile.objects.create_user(
    #         name=validated_data['name'],
    #         bio=validated_data['bio'],
    #         profile_pic=validated_data['profile_pic']
    #     )
    #     return profile    
        
    
class UserSerializer(serializers.ModelSerializer):
    profile = ProfileSerializer()

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'profile']

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
