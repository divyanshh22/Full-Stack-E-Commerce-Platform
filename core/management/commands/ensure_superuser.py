import os

from django.contrib.auth.models import User
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "Create a superuser from ADMIN_* env vars if it does not already exist."

    def handle(self, *args, **options):
        username = os.getenv('ADMIN_USERNAME', 'admin')
        email = os.getenv('ADMIN_EMAIL', 'admin@example.com')
        password = os.getenv('ADMIN_PASSWORD')

        if not password:
            self.stdout.write(self.style.WARNING(
                'ADMIN_PASSWORD not set; skipping superuser creation.'
            ))
            return

        if User.objects.filter(username=username).exists():
            self.stdout.write(self.style.SUCCESS(
                f'Superuser "{username}" already exists.'
            ))
            return

        User.objects.create_superuser(username=username, email=email, password=password)
        self.stdout.write(self.style.SUCCESS(f'Superuser "{username}" created.'))
