from . import views
from django.urls import path

urlpatterns = [
    path("job/<str:slug>/interview/<str:token>/live/", views.interview_live, name="interview_live"),
]
