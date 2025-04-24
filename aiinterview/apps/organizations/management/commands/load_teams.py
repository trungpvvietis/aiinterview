from faker import Faker
from django.core.management.base import BaseCommand

from apps.organizations.models import Department, Team

fake = Faker()

class Command(BaseCommand):

    def handle(self, *args, **kwargs):
        self.stdout.write("Delete Team...")
        Team.objects.all().delete()
        
        self.stdout.write("Creating Team...")
        for department in Department.objects.all():
            for i in range(2):
                Team.objects.create(
                    department=department,
                    name=f"{fake.color_name()} Team",
                )
