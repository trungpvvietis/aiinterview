from django.db import models
from apps.core.models import Timestampable, Slugable, SlugableUnique


class Organization(Timestampable, SlugableUnique):
    logo = models.ImageField(upload_to="organizations/organization-logos", blank=True)
    industry = models.CharField(max_length=100, blank=True)
    is_verified = models.BooleanField(default=False)


class Company(Timestampable, Slugable):
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE)

    class Meta:
        verbose_name_plural = "Companies"


class Department(Timestampable, Slugable):
    company = models.ForeignKey(Company, on_delete=models.CASCADE)


class Team(Timestampable, Slugable):
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
