from faker import Faker
from django.core.management.base import BaseCommand

from apps.organizations.models import Organization

fake = Faker()

class Command(BaseCommand):

    def handle(self, *args, **kwargs):
        self.stdout.write("Delete Organization...")
        Organization.objects.all().delete()
                
        industry_suffixes = ["Technology", "Finance", "Construction", "Digital", "Education"]
        self.stdout.write("Creating Organization...")
        for item in range(5):
            Organization.objects.create(
                name=fake.company(),
                industry=fake.random_element(industry_suffixes),
                is_verified=True,
            )
