from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model

User = get_user_model()

class Command(BaseCommand):

    def handle(self, *args, **options):
    
        self.stdout.write(f"Delete Superuser...")
        User.objects.filter(is_superuser=True).delete()
        User.objects.filter(username="admin").delete()
        
        self.stdout.write(f"Creating Superuser...")
        User.objects.create_user(
            username="admin",
            email="admin@gmail.com",
            password='admin',
            is_staff=True,
            is_superuser=True,
        )
