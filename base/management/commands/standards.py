from django.core.management.base import BaseCommand
from base.models_loc import standardMaker, maker_reset  # Adjust the import path as necessary
class Command(BaseCommand):
    help = 'Creates Standard objects'
    def handle(self, *args, **kwargs):
        maker_reset()