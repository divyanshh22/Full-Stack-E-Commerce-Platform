import os

from django.contrib.sites.models import Site
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "Set the Site domain/name used by django-allauth from environment variables."

    def handle(self, *args, **options):
        domain = os.getenv('SITE_DOMAIN') or os.getenv('ALLOWED_HOSTS', 'localhost').split(',')[0].strip()
        name = os.getenv('SITE_NAME', domain)

        site, _ = Site.objects.get_or_create(pk=1)
        site.domain = domain
        site.name = name
        site.save()

        self.stdout.write(self.style.SUCCESS(f"Site set to {site.domain} ({site.name})"))
