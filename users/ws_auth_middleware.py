from channels.db import database_sync_to_async
from django.contrib.auth.models import User
from rest_framework.exceptions import PermissionDenied
from rest_framework_simplejwt.tokens import AccessToken

@database_sync_to_async
def get_user(id):
    try:
        return User.objects.get(id=id)
    except User.DoesNotExist:
        return None

class WsAuthMiddleware:

    def __init__(self, app):
        self.app = app
        
        
    async def authenticate(self, scope):
        query_string = scope.get('query_string', None)
        if not query_string or query_string == '':
            return None
        try:
            token = query_string.decode('utf-8').strip().split('=')[1]
            access_token = AccessToken(token)
            payload = access_token.payload
            access_token.verify()
            # print('payload : ', payload)
            return await get_user(payload.get('user_id'))
        except Exception as e:
            print(e)
            return None        
        
            
    async def __call__(self, scope, receive, send):
        user = await self.authenticate(scope)
        scope['user'] = user
        return await self.app(scope, receive, send)
    