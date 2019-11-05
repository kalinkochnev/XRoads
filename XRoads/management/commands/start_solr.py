from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "Starts the solr server"

    def handle(self, *args, **options):
