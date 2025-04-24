from django.core.management.base import BaseCommand
from apps.jobs.models import Job


class Command(BaseCommand):

    def handle(self, *args, **options):
        self.stdout.write(f"Delete Job...")
        Job.objects.all().delete()

        self.stdout.write(f"Creating Job...")
