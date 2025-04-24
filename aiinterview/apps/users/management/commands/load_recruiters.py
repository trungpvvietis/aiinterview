from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from faker import Faker
from apps.users.models import RecruiterProfile
from apps.organizations.models import Organization, Company, Department, Team

fake = Faker()
User = get_user_model()

class Command(BaseCommand):

    def handle(self, *args, **options):
        recruiter_count = 20
        
        self.stdout.write(f"Delete RecruiterProfile...")
        User.objects.filter(recruiterprofile__isnull=False).delete()

        orgs = list(Organization.objects.all())
        companies = list(Company.objects.all())
        departments = list(Department.objects.all())
        teams = list(Team.objects.all())

        self.stdout.write(f"Creating {recruiter_count} RecruiterProfile...")
        for _ in range(recruiter_count):
            try:
                user = User.objects.create_user(
                    username=fake.user_name(),
                    email=fake.email(),
                    password='matkhau123'
                )
                RecruiterProfile.objects.create(
                    user=user,
                    phone=fake.phone_number(),
                    organization=fake.random_element(orgs),
                    company=fake.random_element(companies),
                    department=fake.random_element(departments),
                    team=fake.random_element(teams),
                )
            except Exception:
                pass
