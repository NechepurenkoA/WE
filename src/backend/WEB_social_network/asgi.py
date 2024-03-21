import os

from channels.routing import ProtocolTypeRouter, URLRouter
from channels.security.websocket import AllowedHostsOriginValidator
from django.core.asgi import get_asgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "WEB_social_network.settings")
django_asgi_application = get_asgi_application()

import chat.routing  # noqa
from WEB_social_network.tokenauth_middleware import TokenAuthMiddleware  # noqa

application = ProtocolTypeRouter(
    {
        "http": django_asgi_application,
        "websocket": AllowedHostsOriginValidator(
            TokenAuthMiddleware(URLRouter(chat.routing.websocket_urlpatterns))
        ),
    }
)
