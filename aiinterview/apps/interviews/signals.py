from django.db.models.signals import post_save
from django.dispatch import receiver
from apps.interviews.models import Interview
from .tasks import scoring_resume_job_task


@receiver(post_save, sender=Interview)
def handle_iterview_post_save(sender, instance, created, **kwargs):
    # Get resume
    resume = instance.user.resume_set.first()
    job = instance.job
    if resume and resume.resume_text and job:
        # Get job
        scoring_resume_job_task.delay(job.id, resume.id)
