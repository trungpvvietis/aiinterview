from django.core.management import call_command
from django.core.management.base import BaseCommand



class Command(BaseCommand):

    def handle(self, *args, **kwargs):
        call_command("load_organizations")
        call_command("load_companies")
        call_command("load_departments")
        call_command("load_teams")

        call_command("load_superuser")
        call_command("load_candidates")
        call_command("load_recruiters")

        call_command("load_prompts")
        
        call_command("load_resumes")
        
        call_command("load_jobs")
