from rest_framework.views import APIView
from rest_framework.generics import ListAPIView
from .models import FriendRequest
from django.contrib.auth.models import User
from chats.models import Friend
from users.models import Profile
from users.serializers import ProfileSerializer
from .serializers import FriendRequestSerializer
from .models import FriendRequest
from rest_framework.response import Response
from helper.choices import PENDING, SUCCESS

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
        ## send new updated data
        data = ProfileSerializer(to_user.profile, context = {'request' : request}).data
        return Response(data)        

class HandleDeclineOrAcceptRequest(APIView):
    
    def post(self, request, request_id, **kwargs):
        accept = self.request.query_params.get('accept') == 'true'
        obj = FriendRequest.objects.get(uiid = request_id)
        if accept:
            obj.status = SUCCESS
            obj.save()
        else:
            obj.delete()
        return Response({"detail" : 'Request accepted!' if accept else 'Request rejected!'})
        


class RequestsView(ListAPIView):
    serializer_class = FriendRequestSerializer
    queryset = FriendRequest.objects.all()
    
    def get_queryset(self):
        queryset = super().get_queryset()
        if self.request.query_params.get('self') == 'true':
            queryset = self.request.user.received_requests.filter(status = PENDING )        
        return queryset