import csv

from django.core.management import BaseCommand

from main.models import School


class Command(BaseCommand):
    help = "Create new schools from CSV file `./manage.py load_schools_from_csv filename.csv`"

    def add_arguments(self, parser):
        parser.add_argument('file_name', type=str, help="Full path of csv file with schools")

    def handle(self, *args, **options):
        file_name = options.get('file_name')
        with open(file_name) as csvfile:
            reader = csv.reader(csvfile)
            num_rows = 0
            for row in reader:
                num_rows += 1
                School.create_or_update_from_csv_row(row)
        self.stdout.write(self.style.SUCCESS('Created or updated all {} rows from {}'.format(num_rows, file_name)))