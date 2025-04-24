from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
from apps.resumes.constants import ResumeParseStatusChoices
from apps.resumes.models import Resume
from .tasks import parse_resume_task
from .helpers import read_resume


@receiver(pre_save, sender=Resume)
def handle_resume_pre_save(sender, instance, **kwargs):
    # Read file
    resume_text = read_resume(instance.file)
    instance.resume_text = resume_text
    return instance


@receiver(post_save, sender=Resume)
def handle_resume_post_save(sender, instance, **kwargs):
    # Parsed data
    if instance.resume_text and instance.parse_status != ResumeParseStatusChoices.PARSED:
        parse_resume_task.delay(instance.id)
