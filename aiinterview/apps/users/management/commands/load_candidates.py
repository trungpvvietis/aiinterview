from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from faker import Faker
from apps.users.models import CandidateProfile

fake = Faker()
User = get_user_model()

class Command(BaseCommand):

    def handle(self, *args, **options):
        self.stdout.write(f"Delete CandidateProfile...")
        User.objects.filter(candidateprofile__isnull=False).delete()
        
        candidate_count = 50
        self.stdout.write(f"Creating {candidate_count} CandidateProfile...")
        for _ in range(candidate_count):
            try:
                user = User.objects.create_user(
                    username=fake.user_name(),
                    email=fake.email(),
                    password='matkhau123'
                )
                CandidateProfile.objects.create(
                    user=user,
                    phone=fake.phone_number(),
                    education=fake.job(),
                    experience_summary=fake.text(max_nb_chars=200),
                    preferred_job_titles=fake.job(),
                    linkedin_url=fake.url()
                )
            except Exception:
                pass
