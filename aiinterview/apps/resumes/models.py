from django.db import models
from django.conf import settings
from apps.core.models import Timestampable
from apps.jobs.models import Job
from .constants import ResumeParseStatusChoices


class Resume(Timestampable):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    file = models.FileField(upload_to="resumes/resume-files")
    is_active = models.BooleanField(default=True)
    parse_status = models.CharField(max_length=15, choices=ResumeParseStatusChoices, default=ResumeParseStatusChoices.PENDING)
    parse_attempts = models.PositiveIntegerField(default=0)
    resume_text = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Resume {self.user}"


class ParsedResumeData(Timestampable):
    resume = models.OneToOneField(Resume, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=100, blank=True, null=True)
    email = models.EmailField(max_length=100, blank=True, null=True)
    phone_number = models.CharField(max_length=100, blank=True, null=True)
    address = models.CharField(max_length=100, blank=True, null=True)
    linkedin_url = models.URLField(blank=True, null=True)
    github_url = models.URLField(blank=True, null=True)
    portfolio_url = models.URLField(blank=True, null=True)
    birthdate = models.DateField(blank=True, null=True)
    total_years_experience = models.IntegerField(null=True, blank=True)
    recent_position = models.CharField(max_length=100, blank=True, null=True)
    recent_company = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return f"Parsed Resume {self.resume.user}"


class CVScoreSummary(Timestampable):
    resume = models.ForeignKey(Resume, on_delete=models.CASCADE)
    job = models.ForeignKey(Job, on_delete=models.CASCADE)
    education_score = models.FloatField(blank=True, null=True)
    skills_score = models.FloatField(blank=True, null=True)
    experience_score = models.FloatField(blank=True, null=True)
    overall_cv_score = models.FloatField(blank=True, null=True)
    
    def __str__(self):
        return f'CV Score Summary of resume {self.resume} for job {self.job}'
