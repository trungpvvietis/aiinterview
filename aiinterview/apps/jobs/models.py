from django.db import models
from django.urls import reverse
from django.conf import settings
from django.contrib.sites.models import Site

from apps.core.models import Timestampable, SlugableUnique
from apps.organizations.models import Organization, Company, Department, Team
from .constants import JobStatusChoices, JobWorkModeChoices, JobSalaryTypeChoices, JobExperienceLevelChoices, JobEmploymentTypeChoices


class Job(Timestampable, SlugableUnique):
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    organization = models.ForeignKey(Organization, on_delete=models.SET_NULL, null=True)
    company = models.ForeignKey(Company, on_delete=models.SET_NULL, null=True)
    department = models.ForeignKey(Department, on_delete=models.SET_NULL, null=True)
    team = models.ForeignKey(Team, on_delete=models.SET_NULL, null=True)
    description = models.TextField()
    status = models.CharField(max_length=10, choices=JobStatusChoices, default=JobStatusChoices.DRAFT)
    work_mode = models.CharField(max_length=10, blank=True, null=True, choices=JobWorkModeChoices)
    salary_type = models.CharField(max_length=10, blank=True, null=True, choices=JobSalaryTypeChoices)
    salary_min = models.DecimalField(max_digits=15, decimal_places=2, blank=True, null=True)
    salary_max = models.DecimalField(max_digits=15, decimal_places=2, blank=True, null=True)
    experience_level = models.CharField(max_length=10, blank=True, null=True, choices=JobExperienceLevelChoices)
    employment_type = models.CharField(max_length=10, blank=True, null=True, choices=JobEmploymentTypeChoices)
    requirements = models.TextField(blank=True)
    published_at = models.DateTimeField(blank=True, null=True)
    closed_at = models.DateTimeField(blank=True, null=True)
    
    def __str__(self):
        return self.name

    def get_share_link(self):
        current_site = Site.objects.get_current()
        if self.slug:
            path = reverse("job_interview_join", kwargs={"slug": self.slug})
            return f"http://{current_site.domain}{path}"
        return None


class JobInterviewConfig(Timestampable):
    job = models.OneToOneField(Job, on_delete=models.CASCADE)
    total_questions = models.IntegerField()
    categories = models.JSONField(default=list, blank=True)
    allow_followups = models.BooleanField(default=True)
    
    def __str__(self):
        return f"Interview Config of job {self.job}"
