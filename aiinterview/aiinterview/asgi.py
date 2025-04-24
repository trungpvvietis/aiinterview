"""
ASGI config for aiinterview project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.2/howto/deployment/asgi/
"""

import os

from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from channels.security.websocket import AllowedHostsOriginValidator
from django.core.asgi import get_asgi_application
from . import routing

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'aiinterview.settings')

application = ProtocolTypeRouter(
    {
        "http": get_asgi_application(),
        'websocket': URLRouter(
            routing.websocket_urlpatterns
        )
    }
)
