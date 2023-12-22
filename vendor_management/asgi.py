"""
ASGI config for vendor_management project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/howto/deployment/asgi/
"""

# import os

# from django.core.asgi import get_asgi_application
from vendor_api.consumers import *
# from django.urls import path
# from channels.routing import ProtocolTypeRouter, URLRouter

# os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'vendor_management.settings')

# application = get_asgi_application()

# ws_patterns = [
#     path('api/vendors/1/performance/',TestConsumer)
# ]

# application = ProtocolTypeRouter({
#     'websocket': URLRouter(ws_patterns)
# })


import os
from django.core.asgi import get_asgi_application
from django.urls import path
from channels.routing import ProtocolTypeRouter, URLRouter
from vendor_api.consumers import *  # Import your consumer

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'vendor_management.settings')

application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": URLRouter(
        [
            path("api/vendors/<int:id>/performance/", VendorPerformanceConsumer.as_asgi()),
            # Add more paths if needed
        ]
    ),
})
