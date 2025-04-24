from django.db import models


class InterviewTypeChoices(models.TextChoices):
    AI = "ai", "AI"
    INPERSON = "inperson", "In-person"


class InterviewStatusChoices(models.TextChoices):
    SCHEDULED = 'scheduled', 'Scheduled'
    IN_PROGRESS = 'in_progress', 'In Progress'
    COMPLETED = 'completed', 'Completed'
    EXPIRED = 'expired', 'Expired'
    CANCELLED = 'cancelled', 'Cancelled'
    SCORED = 'scored', 'Scored'
    REVIEWED = 'reviewed', 'Reviewed'


class InterviewSessionStatusChoices(models.TextChoices):
    WAITING = 'waiting', 'Waiting'
    ACTIVE = 'active', 'Active'
    DISCONNECTED = 'disconnected', 'Disconnected'
    REJOINED = 'rejoined', 'Rejoined'
    COMPLETED = 'completed', 'Completed'
    ABANDONED = 'abandoned', 'Abandoned'
    EXPIRED = 'expired', 'Expired'


class InterviewAnswerMediaTypeChoices(models.TextChoices):
    TEXT = 'text', 'Text'
    AUDIO = 'audio', 'Audio'
    VIDEO = 'video', 'Video'


class InterviewAnswerStatusChoices(models.TextChoices):
    PENDING = 'pending', 'Pending'
    ANSWERED = 'answered', 'Answered'
    SKIPPED = 'skipped', 'Skipped'
    TIMEOUT = 'timeout', 'Timeout'
    INVALID = 'invalid', 'Invalid'
