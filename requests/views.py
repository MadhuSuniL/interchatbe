from rest_framework.views import APIView
from .models import FriendRequest
from django.contrib.auth.models import User
from chats.models import Friend
from users.models import Profile
from users.serializers import ProfileSerializer
from rest_framework.response import Response
from helper.choices import PENDING

class FriendRequestToggleView(APIView):
    
    def post(self, request, *args, **kwargs):
        from_user = request.user
        to_user_username = request.data.get('to_user')
        to_user = User.objects.get(username = to_user_username)
        friend_request, created = FriendRequest.objects.get_or_create(from_user = from_user, to_user = to_user)
        status = friend_request.status
        ## delete request if it was already created
        if not created:
            friend_request.delete()
        ## UnFriend if friend
        if status != PENDING:
            friend = Friend.objects.get(user = from_user, friend = to_user)
            friend.delete()
        ## send new updated data
        data = ProfileSerializer(to_user.profile, context = {'request' : request}).data
        return Response(data)        