import django.conf.urls.static
from helper.consumers import BaseAsyncJsonWebsocketConsumer
from channels.db import database_sync_to_async
from .models import Friend, Message
from .serializers import ChatSerializer, MessageSerializer

class ChatConsumer(BaseAsyncJsonWebsocketConsumer):
    groups = []

    async def connect(self):
        if await self.user_connect():
            await self.channel_layer.group_add('chats', self.channel_name)
            await self.send_user_chats()

    async def receive_json(self, content, **kwargs):
        pass

    @database_sync_to_async
    def get_user_chats(self):
        chats = self.user.user_chats_from.all() | self.user.user_chats_to.all()
        chats_data = ChatSerializer(chats, many = True, context = {'user' : self.user}).data
        chats_data = self.convert_to_list_of_dict(chats_data)
        return chats_data                
    
    async def send_user_chats(self):
        data = await self.get_user_chats()
        await self.send_json({
            'type': 'send_user_chats_data',
            'data': data,
        })

    async def add_user_to_group(self, group = 'main'):
        await self.channel_layer.group_add(group, self.channel_name)
    
    async def remove_user_to_group(self, group = 'main'):
        await self.channel_layer.group_discard(group, self.channel_name)
     
    async def send_user_chats_data(self, event):
        await self.send_json(content = event['data'])    

    async def disconnect(self, close_code):
        if close_code == 4403:
            await self.send_json({"error": "User not found"})
        

        
class MessageConsumer(BaseAsyncJsonWebsocketConsumer):
    groups = []

    @database_sync_to_async
    def set_chat_obj(self):
        chat = Friend.objects.get(uiid = self.chat_uiid)
        self.chat = chat
       

    async def connect(self):
        if await self.user_connect():
            chat_uiid = self.scope.get('url_route').get('kwargs').get('chat_uiid')
            if chat_uiid is None:
                await self.send_msg_and_close("'chat_uiid' not found")
            self.chat_uiid = chat_uiid
            self.group = 'chat_'+ chat_uiid
            await self.set_chat_obj()
            await self.add_user_to_group()
            await self.send_user_chat_msgs_to_group()

        
    async def receive_json(self, content, **kwargs):
        print(content)
        event_type = content.get('event_type')
        event_data = content.get('event_data')
        if event_type is None or event_data is None:
            return self.send_msg_and_close('Invalid event')
        await self.message_operations(event_type, event_data)
    
    # message operations

    async def message_operations(self, event_type, event_data):
        if event_type == 'create':
            if 'ref_message' in event_data:
                message = await self.create_message_with_reply(event_data['ref_message'], event_data['message'])
            else:
                message = await self.create_message(event_data['message'])
            await self.send_data_to_group(message)
        elif event_type == 'edit':
            await self.edit_message(event_data['uiid'], event_data['edit_message'])
            data = await self.get_user_chat_msgs()
            await self.send_data_to_group(data)
        elif event_type == 'delete':
            await self.delete_message(event_data['uiid'])
            data = await self.get_user_chat_msgs()
            await self.send_data_to_group(data)
                    
        elif event_type == 'delete all':
            await self.delete_all_message()
            data = await self.get_user_chat_msgs()
            await self.send_data_to_group(data)

    @database_sync_to_async
    def create_message(self, message):
        message = Message.objects.create(user = self.user, message = message, chat = self.chat)  
        message_data = MessageSerializer(message, context = {'user' : self.user}).data
        message_data = self.convert_to_dict(message_data)
        return message_data
    
    @database_sync_to_async
    def create_message_with_reply(self,ref_message, message):
        ref_message = Message.objects.get(uiid=ref_message)  
        message = Message.objects.create(user = self.user, message = message, chat = self.chat, refference_message = ref_message)  
        self.change_message_status(message)
        message_data = MessageSerializer(message, context = {'user' : self.user}).data
        message_data = self.convert_to_dict(message_data)
        return message_data
        
    @database_sync_to_async
    def edit_message(self, uiid, edited_message):
        message = Message.objects.get(uiid=uiid)  
        message.message = edited_message
        message.save()
        message_data = MessageSerializer(message, context = {'user' : self.user}).data
        message_data = self.convert_to_dict(message_data)
        return message_data
        
    @database_sync_to_async
    def delete_message(self, uiid):
        Message.objects.get(uiid=uiid).delete()  
        return None
        
    @database_sync_to_async
    def delete_all_message(self):
        Message.objects.filter(chat = self.chat).delete()  
        return None
        
    @database_sync_to_async
    def get_user_chat_msgs(self):
        chat_msgs = self.chat.messages.all()
        chat_msgs_data = MessageSerializer(chat_msgs, many = True, context = {'user' : self.user}).data
        chat_msgs_data = self.convert_to_list_of_dict(chat_msgs_data)
        return chat_msgs_data
    
    async def send_user_chat_msgs_to_group(self):
        data = await self.get_user_chat_msgs()
        await self.send_data_to_group(data)
        
    async def send_data_to_group(self, data):
        await self.channel_layer.group_send('chat_' +self.chat_uiid, {
            'type': 'send_user_chat_msgs_data',
            'data': data,
        })
          
    async def add_user_to_group(self, group = None):
        await self.channel_layer.group_add(group if group else self.group, self.channel_name)
        
    async def remove_user_to_group(self,  group = None):
        await self.channel_layer.group_discard(group if group else self.group, self.channel_name)

    async def send_user_chat_msgs_data(self, event):
        await self.send_json(content = event['data'])    

    async def disconnect(self, close_code):
        if close_code == 4403:
            await self.send_json({"error": "User not found"})
        if self.user:
            await self.remove_user_to_group()
        
        
        