from glob import glob
from astropy.table import Table
from django.core.management.base import BaseCommand
from tom import models

class Command(BaseCommand):
    help = "Loads targets of all types from file, augmenting with online catalog data"
    required_fields = ['Local ID', 'Target Type', 'Source']

    def add_arguments(self, parser):
        parser.add_argument("file", type=str, help="Pattern for CSV file(s) to load")

    def handle(self, *_, **options) -> None:
        for file in glob(options["file"]):
            target_list = Table.read(file, format="ascii.csv", converters={"*": str})

            if not set(target_list.colnames).issuperset(set(self.required_fields)):
                self.stderr.write(
                    self.style.ERROR(f"File {file} must contain fields: {", ".join(self.required_fields)}")
                )
                return

            num_created, num_updated = 0, 0
            for row in target_list:
                _, created = models.Target.objects.update_or_create(
                    local_id=row["Local ID"],
                    target_type=row["Target Type"],
                    source=row["Source"],
                )
                if created:
                    num_created += 1
                else:
                    num_updated += 1

            self.stderr.write(
                self.style.SUCCESS(f"Created {num_created} and updated {num_updated} targets from {file}")
            )
