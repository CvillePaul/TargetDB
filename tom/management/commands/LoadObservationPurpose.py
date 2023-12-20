from datetime import datetime, timezone
from astropy.table import Table, join
import astropy.units as u
from django.core.management.base import BaseCommand
from tom import models


class Command(BaseCommand):
    help = "Loads observation purposes from the specified CSV file"
    required_fields = ["Purpose"]

    def add_arguments(self, parser):
        parser.add_argument("file", type=str, help="CSV file to load")

    def handle(self, *_, **options):
        table = Table.read(options["file"], format="ascii.csv")

        # verify we have all the necessary fields
        if not set(table.colnames).issuperset(set(self.required_fields)):
            self.stderr.write(
                self.style.ERROR(
                    f"File must contain fields: {", ".join(self.required_fields)}"
                )
            )
            return

        # turn each row into a database entry
        for row in table:
            purpose = models.ObservationPurpose(purpose=row["Purpose"])
            purpose.save()
        self.stdout.write(
            self.style.SUCCESS(f"Loaded {len(table)} observation purposes")
        )
