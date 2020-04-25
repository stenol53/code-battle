import asyncio
import json
from django.contrib.auth import get_user_model
from channels.consumer import AsyncConsumer
from channels.db import database_sync_to_async

from .models import Battle,Contact,Pair,Task,AnswerVariant

class BattleConsumer(AsyncConsumer):
    async def websocket_connect(self,event):
        print ('connected', event)
        battle_id = self.scope['url_route']['kwargs']['battle_id']
        me = self.scope['user']
        print(battle_id, me)
        battle = await self.get_battle(battle_id)
        print(battle)
        
        await self.send({
            "type": "websocket.accept"
        })
        
    
    async def websocket_receive(self,event):
        print ('receved', event)

    async def websocket_disconnect(self,event):
        print ('disconnected', event)
    
    @database_sync_to_async
    def get_battle(self, battle_id):
        return Battle.objects.get(pk=battle_id)