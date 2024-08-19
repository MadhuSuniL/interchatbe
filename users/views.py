from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import status
from django.db.models import Q, Count
from rest_framework.response import Response
from django.contrib.auth import authenticate
from rest_framework import serializers
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.views import TokenObtainPairView
from .serializers import RegisterSerializer, LoginSerializer, ProfileSerializer
from django.contrib.auth.models import User
from .models import Profile
from chats.models import Friend
from .utils import cosine_similarity
import networkx as nx
import matplotlib.pyplot as plt

##############################################################################################
####################################### EXPLORE USERS #################################################
##############################################################################################

        

        
    
class YouMightKnowAndLikeUsersView(APIView):
    permission_classes = [IsAuthenticated]
    G = nx.Graph()

    def suggest_friends(self, user):
        # friends_objs = Friend.objects.all()
        # for obj in friends_objs:
        #      G.add_edge(obj.user, obj.friend)
        return []

    def get(self, request, *args, **kwargs):
        # Get the current user's bio
        current_user_bio = Profile.objects.get(user = request.user).bio

        # Initialize an empty list to hold similar users
        might_know_users = []

        # Iterate over all profiles to calculate similarity
        for profile in Profile.objects.exclude(user=request.user):
            try:
                similarity = cosine_similarity(current_user_bio, profile.bio)
                if similarity >= 0.5:  # 50% or more similarity
                    might_know_users.append(profile)
            except:
                pass
        
        suggested_friends = self.suggest_friends(request.user)
        for suggest_friend in suggested_friends:
            if suggest_friend not in might_know_users:
                might_know_users.append(suggest_friend)

        # Serialize the profiles
        serializer = ProfileSerializer(Profile.objects.exclude(user=request.user), many=True, context = {'request' : request})
        return Response(serializer.data)

class UserSearchView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        query = request.query_params.get('query')
        if query:
            profiles = Profile.objects.filter(
                Q(user__username__icontains=query) | 
                Q(name__icontains=query) 
            ).exclude(user = request.user)
            serializer = ProfileSerializer(profiles, many=True, context = {'request' : request})
            return Response(serializer.data, status=200)
        return Response([], status=200)

##############################################################################################
####################################### AUTH #################################################
##############################################################################################


class LoginView(APIView):
    permission_classes = [AllowAny]
    authentication_classes = []

    def validate(self, data):
        username = data.get("username")
        password = data.get("password")

        if username and password:
            user = authenticate(username=username, password=password)

            if user is None:
                raise serializers.ValidationError("Invalid credentials.")

            if not user.is_active:
                raise serializers.ValidationError("User is inactive.")
        else:
            raise serializers.ValidationError("Must include 'username' and 'password'.")
        return user
    
    def get_tokens_data(self, user):
        refresh = RefreshToken.for_user(user)
        profile = Profile.objects.get(user = user)
        profile_data = ProfileSerializer(profile, context = {'request' : self.request}).data
        data = {
            'refresh': str(refresh),
            'access': str(refresh.access_token),
            'user_id': user.id,
            'username': user.username,
        }
        data.update(profile_data)
        return data
 
    def post(self, request, *args, **kwargs):
        user = self.validate(request.data)
        tokens_data = self.get_tokens_data(user)
        return Response(tokens_data, status=status.HTTP_200_OK)
        
class RegisterView(APIView):
    permission_classes = [AllowAny]
    authentication_classes = []

    def post(self, request, *args, **kwargs):
        username = request.data.get('username')
        password = request.data.get('password')
        name = request.data.get('name')
        bio = request.data.get('bio')
        profile_pic = request.data.get('profile_pic')
        
        user = User.objects.create_user(username = username, password = password)
        profile, created = Profile.objects.get_or_create(user=user)
        serializer = ProfileSerializer(profile, data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Account registered successfully"}, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)        

class SelfProfile(APIView):
    
    def get(self, request):
        profile = request.user.profile
        data = ProfileSerializer(profile, context = {"request" : request}).data
        return Response(data)

class ProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        profile, created = Profile.objects.get_or_create(user=request.user)
        serializer = ProfileSerializer(profile, context={'request': request})
        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        profile, created = Profile.objects.get_or_create(user=request.user)
        serializer = ProfileSerializer(profile, data=request.data, context={'request': request})
        
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, *args, **kwargs):
        profile, created = Profile.objects.get_or_create(user=request.user)
        serializer = ProfileSerializer(profile, data=request.data, partial=True, context={'request': request})
        
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)