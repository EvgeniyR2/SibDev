from django.conf.urls import url
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.security.websocket import AllowedHostsOriginValidator
from channels.auth import AuthMiddlewareStack

from SibDev.consumers import UrlConsumer

application = ProtocolTypeRouter({
        'websocket': AllowedHostsOriginValidator(
            AuthMiddlewareStack(
                URLRouter([
                    url(r'^$', UrlConsumer)
                ])
            )
        )
    })
