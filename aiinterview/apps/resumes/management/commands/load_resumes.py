from django.core.management.base import BaseCommand
from apps.resumes.models import Resume
from django.contrib.auth import get_user_model
from faker import Faker
from apps.resumes.constants import ResumeParseStatusChoices
import random

fake = Faker()
User = get_user_model()

class Command(BaseCommand):

    def handle(self, *args, **options):
        self.stdout.write(f"Delete Resume...")
        Resume.objects.all().delete()

        resume_count = 10
        self.stdout.write(f"Creating Resume...")
        for _ in range(resume_count):
            users = User.objects.filter(candidateprofile__isnull=False)
            user = random.choice(users)

            Resume.objects.create(
                user=user,
                is_active=random.choice([True, False]),
                parse_status=random.choice([
                    ResumeParseStatusChoices.PENDING,
                    ResumeParseStatusChoices.PARSED,
                    ResumeParseStatusChoices.FAILED,
                ]),
                parse_attempts=random.randint(0, 3)
            )
