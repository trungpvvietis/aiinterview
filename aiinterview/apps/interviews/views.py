from django.shortcuts import render

from apps.interviews.models import InterviewSession, Interview
from apps.jobs.models import Job
from .models import Interview, InterviewQuestion
from .constants import InterviewSessionStatusChoices


def interview_live(request, slug, token):
     candidate = request.user
     job = Job.objects.get(slug=slug)
     interview = Interview.objects.get(share_token=token)
     interview_session, _ = InterviewSession.objects.update_or_create(
          user=candidate,
          interview=interview,
     )
     questions = InterviewQuestion.objects.filter(interview=interview, triggered_by_answer_id=None).order_by("id")
     return render(request, "interviews/interview_live.html", {
         "candidate": candidate,
         "job": job,
         "interview": interview,
         "interview_session": interview_session,
         "questions": questions,
    })
