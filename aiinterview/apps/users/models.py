from django.db import models
from django.conf import settings
from apps.core.models import Timestampable
from apps.organizations.models import Organization, Company, Department, Team


class UserProfile(Timestampable):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    phone = models.CharField(max_length=20, blank=True)

    class Meta:
        abstract = True


class CandidateProfile(UserProfile):
    avatar = models.ImageField(upload_to="users/candidateprofile-avatars/", blank=True)
    education = models.CharField(max_length=100, blank=True)
    experience_summary = models.TextField(blank=True)
    preferred_job_titles = models.CharField(max_length=100, blank=True)
    linkedin_url = models.URLField(blank=True)

    def __str__(self):
        return f"Candidate - {self.user}"


class RecruiterProfile(UserProfile):
    avatar = models.ImageField(upload_to="users/recruiteprofile-avatars/", blank=True)
    organization = models.ForeignKey(Organization, on_delete=models.SET_NULL, null=True)
    company = models.ForeignKey(Company, on_delete=models.SET_NULL, null=True)
    department = models.ForeignKey(Department, on_delete=models.SET_NULL, null=True)
    team = models.ForeignKey(Team, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return f"Recruiter - {self.user}"
