from django.shortcuts import render

from apps.interviews.models import InterviewSession, Interview
from apps.jobs.models import Job
from .models import Interview, InterviewQuestion, InterviewScoreSummary
from apps.resumes.models import CVScoreSummary


def interview_live(request, slug, token):
     candidate = request.user
     resume = candidate.resume_set.first()
     job = Job.objects.get(slug=slug)
     interview = Interview.objects.get(share_token=token)
     interview_session, _ = InterviewSession.objects.update_or_create(
          user=candidate,
          interview=interview,
     )
     questions = InterviewQuestion.objects.filter(interview=interview, triggered_by_answer_id=None).order_by("id")
     scoring_resume_job = CVScoreSummary.objects.filter(job=job, resume=resume).first()
     scoring_interview = InterviewScoreSummary.objects.filter(interview=interview).first()
     return render(request, "interviews/interview_live.html", {
         "candidate": candidate,
         "job": job,
         "interview": interview,
         "interview_session": interview_session,
         "questions": questions,
         "scoring_resume_job": scoring_resume_job,
         "scoring_interview": scoring_interview,
    })
