from faker import Faker
from django.core.management.base import BaseCommand

from apps.organizations.models import Company, Department

fake = Faker()

class Command(BaseCommand):

    def handle(self, *args, **kwargs):
        self.stdout.write("Delete Department...")
        Department.objects.all().delete()
        
        self.stdout.write("Creating Department...")
        for company in Company.objects.all():
            for i in range(2):
                Department.objects.create(
                    company=company,
                    name=fake.bs().title()
                )
