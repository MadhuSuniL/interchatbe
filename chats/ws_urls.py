from django.urls import path
from .consumers import MessageConsumer

urlpatterns = [
    # path('ws/chats', ChatConsumer.as_asgi()),
    path('ws/messages/<chat_uiid>', MessageConsumer.as_asgi())
]