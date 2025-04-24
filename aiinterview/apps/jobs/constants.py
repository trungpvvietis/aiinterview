from django.db import models


class JobStatusChoices(models.TextChoices):
    DRAFT = "draft", "Draft"
    PUBLISHED = "published", "Published"


class JobWorkModeChoices(models.TextChoices):
    ONSITE = "onsite", "On-site"
    REMOTE = "remote", "Remote"
    HYBRID = "hybrid", "Hybrid"


class JobSalaryTypeChoices(models.TextChoices):
    FIXED = "fixed", "Fixed"
    RANGE = "range", "Range"


class JobExperienceLevelChoices(models.TextChoices):
    JUNIOR = "junior", "Junior"
    MID = "mid", "Mid"
    SENIOR = "senior", "Senior"


class JobEmploymentTypeChoices(models.TextChoices):
    FULLTIME = "fulltime", "Full-time"
    PARTTIME = "parttime", "Part-time"
    CONTRACT = "contract", "Contract"
    INTERNSHIP = "internship", "Internship"