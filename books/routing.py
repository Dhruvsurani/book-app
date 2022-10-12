

# from django.urls import re_path
#
# from . import consumers
#
# websocket_urlpatterns = [
#      re_path('stories/notification_testing/', consumers.NotificationConsumer.as_asgi()),
#  ]

# import os
# from channels.routing import ProtocolTypeRouter, URLRouter
# from channels.auth import AuthMiddlewareStack
# # from stories import consumers
#
# from django.urls import re_path, path
# from django.core.asgi import get_asgi_application
#
# os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'bookapp1.settings')
#
# application = ProtocolTypeRouter({
#     "http": get_asgi_application(),
#     "websocket": AuthMiddlewareStack(
#         URLRouter(
#             [path('stories/notification_testing/', consumers.NotificationConsumer.as_asgi())]
#         ))
#
# })