from datetime import datetime, timezone
from astropy.table import Table, join
import astropy.units as u
from django.core.management.base import BaseCommand
from tom import models


class Command(BaseCommand):
    help = "Loads observation purposes from the specified CSV file"
    required_fields = ["First Name", "Last Name", "Email", "Affiliation"]

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
            person = models.Person(
                first_name=row["First Name"],
                last_name=row["Last Name"],
                email=row["Email"],
                affiliation=row["Affiliation"],
            )
            person.save()
        self.stdout.write(self.style.SUCCESS(f"Loaded {len(table)} people"))
