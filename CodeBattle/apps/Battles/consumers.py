import asyncio
import json
from django.contrib.auth import get_user_model
from channels.consumer import AsyncConsumer
from channels.db import database_sync_to_async
from django.db.models import Q

from .models import Battle, Participent, Round, Task, AnswerVariant


class BattleConsumer(AsyncConsumer):
    async def websocket_connect(self, event):
        print('connected', event)

        battle_id = self.scope['url_route']['kwargs']['battle_id']

        me = self.scope['user']
        self.me = me

        battle = await self.get_battle(battle_id)
        self.battle = battle

        # opponent = await self.get_opponent()
        # self.opponent = opponent

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

    async def websocket_receive(self, event):
        print('receved', event)

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
    async def websocket_log(self, event):
        front_response = event.get('text', None)
        print(front_response)

        Response = {}
        good = False
        if front_response is not None:
            json_response = json.loads(front_response)
            print(json_response)
            print(json_response["type"])
            if json_response["type"] == "ready":
                if json_response['ready'] == True:  # Делаем пользователя готовым
                    # Делаем себя готовым в базе
                    need_response = await self.make_user_ready(int(json_response['id']), True)

                    opp = await self.get_opponent()
                    if need_response is not -1:
                        if need_response is not None:
                            if need_response:
                                if opp is not None:
                                    Response = {
                                        'type': 'session',
                                        'id': opp.id,
                                        'start_session': True,
                                        'other_user_name': opp.name,
                                        'other_sername' : opp.sirname,
                                        'other_login' : opp.username,
                                        'questions_count': self.battle.count,
                                    }
                                    good = True
                                else:
                                    Response = {
                                        'type': 'error',
                                        'id': json_response['id'],
                                        'opponent_leave': True
                                    }
                                    good = True
                        else:
                            Response = {
                                'type': 'error',
                                'id': json_response['id'],
                                'opponent_leave': True
                            }
                            good = True
            if json_response["type"] == "session":
                print(json_response)
                opp = await self.get_opponent()
                if json_response["id"] == self.me.id:
                    Response = {
                        'type': 'session',
                        'id': self.me.id,
                        'start_session': True,
                        'other_user_name': opp.name,
                        'other_sername' : opp.sirname,
                        'other_login' : opp.username,
                        'questions_count': self.battle.count,
                    }
                    good = True

            elif json_response["type"] == "question":
                if json_response["method"] == "next":

                    question_ID = json_response["question_num"]

                    if question_ID < self.battle.count:
                        get_question_data = await self.get_question(question_ID, int(json_response["id"]))
                        if get_question_data is not None:
                            if get_question_data is not False:

                                rnd = await self.get_round()
                                await self.save_round_question_num(rnd,question_ID)

                                av_count = get_question_data.av_count
                                av_lst = list()

                                for i in range(0, av_count):
                                    av_data = await self.get_answer_variant(get_question_data, i)
                                    if av_data is not None:
                                        av_lst.append(av_data.text)
                                Response = {
                                    'type': 'question',
                                    'method': 'new',
                                    'id': self.me.id,
                                    'message': get_question_data.question,
                                    'answer_variant': av_lst,
                                    'answer_end_date': self.battle.task_time
                                }
                                good = True

        if good:
            await self.send({
                'type': 'websocket.send',
                'text': json.dumps(Response),
            })
    async def websocket_disconnect(self, event):
        print('disconnected', event)


    @database_sync_to_async
    def save_round_question_num(self,rnd,question_ID):
        if rnd is not None:
            rnd.current_task = question_ID
            rnd.save()
        #     return True
        # return False

    @database_sync_to_async
    def get_question(self, question_id, acc_id):
        if acc_id == self.me.id:
            try:
                qs = Task.objects.get(Battle=self.battle, t_id= question_id)
            except Task.DoesNotExist:
                return None
            return qs
        else:
            return False

    @database_sync_to_async
    def get_answer_variant(self, task, id):
        try:
            res = AnswerVariant.objects.get(Task=task, t_id=id)
        except AnswerVariant.DoesNotExist:
            res = None
        return res

    # Возвращает True, если оба участника подтвердили готовность, иначе False
    @database_sync_to_async
    def make_user_ready(self, user_id, ready):
        if user_id == self.me.id:
            # Ставим готовность
            qs = Participent.objects.get(Battle=self.battle, User = user_id)
            if qs is not None:
                print("good")
                qs.isReady = ready
                qs.save()

            # Получаем оппонента
            user = self.me
            try:
                opp = Round.objects.get(Battle=self.battle, user1=user)
            except Round.DoesNotExist:
                opp = None
            if opp is not None:
                user2 = opp.user2
            else:
                try:
                    opp = Round.objects.get(Battle=self.battle, user2=user)
                except Round.DoesNotExist:
                    opp = None
                user2 = opp.user1

            qs = Participent.objects.get(Battle=self.battle, User = user2)
            if qs is None:
                return None
            return ready and qs.isReady
        return -1

    @database_sync_to_async
    def get_opponent(self):
        # Получаем оппонента
        user = self.me
        try:
            opp = Round.objects.get(Battle=self.battle, user1=user)
        except Round.DoesNotExist:
            opp = None
        if opp is not None:
            user2 = opp.user2
        else:
            try:
                opp = Round.objects.get(Battle=self.battle, user2=user)
            except Round.DoesNotExist:
                opp = None
            user2 = opp.user1
        return user2

    @database_sync_to_async
    def get_battle(self, battle_id):
        return Battle.objects.get(pk=battle_id)

    @database_sync_to_async
    def get_event_caption(self, battle):
        return battle.event.event_title

    @database_sync_to_async
    def get_round(self):
        # Получаем раунд
        user = self.me
        try:
            opp = Round.objects.get(Battle=self.battle, user1=user)
        except Round.DoesNotExist:
            opp = None
        if opp is not None:
            user2 = opp.user2
        else:
            try:
                opp = Round.objects.get(Battle=self.battle, user2=user)
            except Round.DoesNotExist:
                opp = None
        return opp
