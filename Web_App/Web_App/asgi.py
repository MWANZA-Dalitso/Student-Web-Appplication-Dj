import os
from channels.routing import ProtocolTypeRouter, URLRouter # type: ignore
from django.core.asgi import get_asgi_application
from channels.auth import AuthMiddlewareStack # type: ignore
import chat.routing

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myproject.settings')

application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": AuthMiddlewareStack(
        URLRouter(
            chat.routing.websocket_urlpatterns
        )
    ),
})
