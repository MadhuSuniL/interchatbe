from django.urls import path
from .views import FriendRequestToggleView, RequestsView, HandleDeclineOrAcceptRequest

urlpatterns = [
    path('friend-requests/', RequestsView.as_view(), name = 'Friend Request'),    
    path('accept-or-reject/<str:request_id>', HandleDeclineOrAcceptRequest.as_view(), name = 'Friend Request'),    
    path('friend-request-toggle', FriendRequestToggleView.as_view(), name = 'Friend Request')    
]