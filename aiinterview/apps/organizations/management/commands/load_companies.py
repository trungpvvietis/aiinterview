from faker import Faker
from django.core.management.base import BaseCommand

from apps.organizations.models import Organization, Company

fake = Faker()

class Command(BaseCommand):

    def handle(self, *args, **kwargs):
        self.stdout.write("Delete Company...")
        Company.objects.all().delete()
        
        self.stdout.write("Creating Company...")
        for org in Organization.objects.all():
            for i in range(2):
                Company.objects.create(
                    organization=org,
                    name=f"{fake.last_name()} Group",
                )
