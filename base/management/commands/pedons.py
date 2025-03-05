from django.core.management.base import BaseCommand
from base.models_loc import pedonMaker  # Adjust the import path as necessary
from base.models import Source
class Command(BaseCommand):
    help = 'Fills the pedon database'
    def add_arguments(self, parser):
        # Add argument for input
        parser.add_argument('name', type=str, help='The name of the source you want to add.')
    def handle(self, *args, **kwargs):
        name = kwargs['name']
        source = Source.objects.get(name = name)
        pedonMaker(source)