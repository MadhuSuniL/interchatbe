from channels.generic.websocket import AsyncJsonWebsocketConsumer
from uuid import UUID
from collections import OrderedDict

class BaseAsyncJsonWebsocketConsumer(AsyncJsonWebsocketConsumer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
    
    async def user_connect(self):
        user = self.scope.get('user')
        if user is None:
            await self.close(code=4403)  
            return False
        else:
            await self.accept()
            self.user = self.scope.get('user')
            return True

    def convert_to_list_of_dict(self, data):
        if isinstance(data, UUID):
            return str(data)
        elif isinstance(data, OrderedDict):
            return dict((key, self.convert_to_list_of_dict(value)) for key, value in data.items())
        elif isinstance(data, list):
            return [self.convert_to_list_of_dict(item) for item in data]
        else:
            return data
            
    def convert_to_dict(self, data):
        if isinstance(data, UUID):
            return str(data)
        elif isinstance(data, OrderedDict):
            return {key: self.convert_to_dict(value) for key, value in data.items()}
        else:
            return data

    async def send_msg_and_close(self, msg = '', code = 1001):
        await self.send_json({'detail' : msg})
        await self.close(code=code)