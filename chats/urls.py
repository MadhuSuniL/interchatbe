from django.urls import path
from .views import *

urlpatterns = [
    path('friends/', ChatListView.as_view())
]