from django.core.management.base import BaseCommand
from base.models import Source
class Command(BaseCommand):
    help = 'Removes a Source, and its associated datasets, synonyms, sites, and pedons'
    def add_arguments(self, parser):
        # Add argument for input
        parser.add_argument('name', type=str, help='The name of the source you want to remove.')
    def handle(self, *args, **kwargs):
        name = kwargs['name']
        source = Source.objects.get(name = name)
        source.delete()