from django.shortcuts import get_object_or_404
from django.shortcuts import render
from .models import Job
from apps.interviews.models import Interview
from apps.interviews.constants import InterviewTypeChoices, InterviewStatusChoices

def job_interview_join(request, slug):
    candidate = request.user
    job = get_object_or_404(Job, slug=slug)
    interview, _ = Interview.objects.update_or_create(
        user=candidate,
        job=job,
        defaults={
            "interview_type": InterviewTypeChoices.AI,
            "status": InterviewStatusChoices.SCHEDULED,
        }
    )
    return render(request, "jobs/job_interview_join.html", {
        "candidate": candidate,
        "job": job,
        "interview": interview,
    })
