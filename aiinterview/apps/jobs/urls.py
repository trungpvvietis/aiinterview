from . import views
from django.urls import path

urlpatterns = [
    path("job/<str:slug>/interview/join", views.job_interview_join, name="job_interview_join"),
]
