import os
import django
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
import environ

# Initialize environment variables
env = environ.Env(DEBUG=(bool, False))
environ.Env.read_env()  # loads .env file if present

# Set DJANGO_SETTINGS_MODULE before importing anything else
os.environ.setdefault(
    "DJANGO_SETTINGS_MODULE",
    env("DJANGO_SETTINGS_MODULE", default="game_backend.settings")
)

# Setup Django
django.setup()

# Now it’s safe to import modules that rely on Django settings
import game.routing

application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": AuthMiddlewareStack(
        URLRouter(
            game.routing.websocket_urlpatterns
        )
    ),
})
