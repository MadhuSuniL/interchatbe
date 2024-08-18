from rest_framework.generics import ListAPIView
from django.db.models import Q
from .serializers import ChatSerializer
from .models import Friend

class ChatListView(ListAPIView):
    
    serializer_class = ChatSerializer
    queryset = Friend.objects.all()
    
    def get_queryset(self):
        queryset = super().get_queryset()
        if self.request.query_params.get('self') == 'true':
            queryset = Friend.objects.filter(Q(user = self.request.user) | Q(friend = self.request.user))
        return queryset
    