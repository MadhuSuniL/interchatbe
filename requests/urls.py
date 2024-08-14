from django.urls import path
from .views import FriendRequestToggleView

urlpatterns = [
    path('friend-request-toggle', FriendRequestToggleView.as_view(), name = 'Friend Request')    
]