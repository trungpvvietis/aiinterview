import uuid 
import secrets
from django.conf import settings
from django.db import models
from apps.core.models import Timestampable
from apps.jobs.models import Job
from .constants import InterviewTypeChoices, InterviewStatusChoices, InterviewSessionStatusChoices, InterviewAnswerMediaTypeChoices, InterviewAnswerStatusChoices


class Interview(Timestampable):
    slug = models.SlugField(default=uuid.uuid4, unique=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    job = models.ForeignKey(Job, on_delete=models.SET_NULL, null=True)
    interview_type = models.CharField(max_length=20, choices=InterviewTypeChoices, default=InterviewTypeChoices.AI)
    status = models.CharField(max_length=20, choices=InterviewStatusChoices, default=InterviewStatusChoices.SCHEDULED)
    scheduled_at = models.DateTimeField(blank=True, null=True)
    
    share_token = models.CharField(max_length=40, unique=True, blank=True, null=True)
    
    def __str__(self):
        return f"Interview {self.user} of job {self.job}"

    def save(self, *args, **kwargs):
        if not self.share_token:
            self.share_token = secrets.token_urlsafe(16)
        super().save(*args, **kwargs)


class InterviewSession(Timestampable):
    slug = models.SlugField(default=uuid.uuid4, unique=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    interview = models.ForeignKey(Interview, on_delete=models.SET_NULL, null=True)
    status = models.CharField(max_length=15, choices=InterviewSessionStatusChoices, default=InterviewSessionStatusChoices.WAITING)
    is_reconnect = models.BooleanField(default=False)
    
    def __str__(self):
        return f"Interview Session user {self.user} of interview {self.interview}"


class InterviewQuestion(Timestampable):
    interview = models.ForeignKey(Interview, on_delete=models.SET_NULL, null=True)
    question_text = models.TextField(blank=True, null=True)
    question_image = models.ImageField(upload_to="interviews/interview-questions/", blank=True, null=True)
    category = models.CharField(max_length=100, blank=True)
    order_index = models.IntegerField(blank=True, null=True)
    question_type = models.CharField(max_length=100, blank=True, null=True)
    generated_by_ai = models.BooleanField(default=True)
    follow_up_to_id = models.ForeignKey('self', on_delete=models.CASCADE, blank=True, null=True)
    triggered_by_answer_id = models.ForeignKey('InterviewAnswer', on_delete=models.CASCADE, blank=True, null=True)
    weight = models.FloatField(null=True, blank=True)
    trigger_keywords = models.JSONField(blank=True, default=list)
    time_limit_seconds = models.PositiveIntegerField(blank=True, null=True)
    score_threshold = models.FloatField(blank=True, null=True)

    def __str__(self):
        return f"Interview Question of interview {self.interview}"


class InterviewAnswer(Timestampable):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    interview = models.ForeignKey(Interview, on_delete=models.SET_NULL, null=True)
    question = models.ForeignKey(InterviewQuestion, on_delete=models.SET_NULL, null=True)
    answer_text = models.TextField(blank=True, null=True)
    transcript_text = models.TextField(blank=True, null=True)
    media_type = models.CharField(max_length=15, null=True, choices=InterviewAnswerMediaTypeChoices, default=InterviewAnswerMediaTypeChoices.VIDEO)
    media_file = models.FileField(upload_to="interviews/interview-answers/", blank=True, null=True)
    status = models.CharField(max_length=15, choices=InterviewAnswerStatusChoices, default=InterviewAnswerStatusChoices.PENDING)
    expected_answer = models.TextField(blank=True, null=True)
    scoring_guideline = models.TextField(blank=True, null=True)
    feedback_notes = models.TextField(blank=True, null=True)
    ai_tags = models.JSONField(blank=True, default=list)
    ai_score = models.FloatField(blank=True, null=True)
    score_override = models.FloatField(blank=True, null=True)
    final_score = models.FloatField(blank=True, null=True)

    def __str__(self):
        return f"Interview Answer {self.user} for interview {self.interview}"


class InterviewScoreSummary(Timestampable):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    interview = models.ForeignKey(Interview, on_delete=models.SET_NULL, null=True)
    communication_score = models.FloatField(blank=True, null=True)
    challenge_score = models.FloatField(blank=True, null=True)
    appearance_score = models.FloatField(blank=True, null=True)
    facial_score = models.FloatField(blank=True, null=True)
    body_language_score = models.FloatField(blank=True, null=True)
    environment_score = models.FloatField(blank=True, null=True)
    overall_score = models.FloatField(blank=True, null=True)
    summary_feedback = models.TextField(blank=True)

    def __str__(self):
        return f"Interview score summary {self.user} of {self.interview}"
