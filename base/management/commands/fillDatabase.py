from django.core.management.base import BaseCommand
from base.models_loc import maker  # Adjust the import path as necessary
import sys
import traceback
ISCN = {"name" : "ISCN"}
NRCS = {"name" : "RaCA"}
KSSL = {"name" : "KSSL"}
class Command(BaseCommand):
    help = 'Fills the database'
    def add_arguments(self, parser):
        # Add argument for input
        parser.add_argument('name', type=str, help='The name of the source you want to add.')

    def handle(self, *args, **kwargs):
        log_file = 'output_log.txt'
        names = kwargs['name'].split(", ")
        # Redirect the standard output to the log file
        sys.stdout = open(log_file, 'w')
        sys.stdout.write("Starting to fill the database...")
        try:
            for name in names:
                n_name = name.split("_")
                maker({"name" : n_name[0], "type" : n_name[1]})
            sys.stdout.write(self.style.SUCCESS('Successfully filled the database'))
        except Exception as e:
            # Catch and log any exception
            print(f"Exception raised: {str(e)}")
            # Log the traceback for debugging purposes
            traceback.print_exc(file=sys.stdout)
        finally:
            sys.stdout.close()
        