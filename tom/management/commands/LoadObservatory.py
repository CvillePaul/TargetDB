from astropy.table import Table
from django.core.management.base import BaseCommand
from tom import models


class Command(BaseCommand):
    help = "Loads observatories from the specified CSV file"
    required_fields = ["Nickname", "Name", "IAU Code"]

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
            observatory = models.Observatory(
                nickname=row["Nickname"], name=row["Name"], iau_code=row["IAU Code"]
            )
            observatory.save()
        self.stdout.write(self.style.SUCCESS(f"Loaded {len(table)} observatories"))
