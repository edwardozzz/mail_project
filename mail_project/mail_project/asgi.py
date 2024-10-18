import os
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
import mail_integration.routing

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mail_project.settings')

application = ProtocolTypeRouter({
    'http': get_asgi_application(),
    'websocket': AuthMiddlewareStack(
        URLRouter(
            mail_integration.routing.websocket_urlpatterns
        )
    ),
})
