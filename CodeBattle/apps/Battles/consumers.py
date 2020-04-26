import asyncio
import json
from django.contrib.auth import get_user_model
from channels.consumer import AsyncConsumer
from channels.db import database_sync_to_async

from .models import Battle, Participent

class BattleConsumer(AsyncConsumer):
    async def websocket_connect(self,event):
        print ('connected', event)

        battle_id = self.scope['url_route']['kwargs']['battle_id']
        me = self.scope['user']
        self.me = me
        print(battle_id, me)
        battle = await self.get_battle(battle_id)
        self.battle = battle
        battle_room = "battle_"+str(battle_id)

        self.battle_room = battle_room
        await self.channel_layer.group_add(
            battle_room,
            self.channel_name
        )
        await self.send({
            "type": "websocket.accept"
        })
        # await self.send({
        #     "type": "websocket.send",
        #     "text": await self.get_event_caption(battle)
        # })
        
        
    
    async def websocket_receive(self,event):
        print ('receved', event)

        # data = { 
        #     'user_id': self.me.id,
        #     'ready': True
        # }

        event = {
            'type': 'websocket_log',
            'text': event['text']
        }

        await self.channel_layer.group_send(
            self.battle_room,
            event
        )




    async def websocket_log(self,event):
        front_response = event.get('text',None)
        print(front_response)

        Response = {}
        good = True;
        if front_response is not None:  
            json_response = json.loads(front_response);
            print(json_response)
            print(json_response["type"])
            if json_response["type"] == "ready":
                print(2)
                if json_response['ready'] == True:

                    print(3)
                    await self.get_user_from_battle(int(json_response['id']))
                    # print(qs)


                    Response = {
                        'id' : json_response['id'],
                        'ready' : True
                    }
                else:
                    Response = {
                        'id' : json_response['id'],
                        'ready' : False
                    }


        if good:
            await self.send({
            'type': 'websocket.send',
            'text': json.dumps(Response),
            })






    async def websocket_disconnect(self,event):
        print ('disconnected', event)

    @database_sync_to_async
    def get_user_from_battle(self,user_id):
        qs = Participent.objects.get(Battle = self.battle,User = user_id)
        if qs is not None: 
            print("good")
            qs.isReady = True
            qs.Save()
        
        
        
    
    @database_sync_to_async
    def get_battle(self, battle_id):
        return Battle.objects.get(pk=battle_id)

    @database_sync_to_async
    def get_event_caption(self, battle):
        return battle.event.event_title