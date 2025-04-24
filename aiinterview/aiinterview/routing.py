from django.urls import re_path
from apps.interviews import consumers

websocket_urlpatterns = [
    re_path(r"^ws/interview/(?P<session_id>[^/]+)/$", consumers.InterviewConsumer.as_asgi()),
]
