from channels.routing import ProtocolTypeRouter, URLRouter
from django.conf.urls import url
from channels.auth import AuthMiddlewareStack
from channels.security.websocket import AllowedHostsOriginValidator, OriginValidator

# from CodeBattle.apps.Battles.consumers import BattleConsumer

application = ProtocolTypeRouter({
    # Empty for now (http->django views is added by default)
    'websocket': AllowedHostsOriginValidator (
        AuthMiddlewareStack (
            URLRouter (
                 [
                    #  url(r"^battle/(?P<battle_id>\w)/$", BattleConsumer),
                 ]
            )
        )

    )
})