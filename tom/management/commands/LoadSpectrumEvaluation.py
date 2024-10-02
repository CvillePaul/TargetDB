from datetime import datetime, timezone
from glob import glob
from astropy.table import Table
import astropy.units as u
from django.core.management.base import BaseCommand
from tom import models


class Command(BaseCommand):
    help = "Loads speckle observations from the specified CSV file"
    required_fields = [
        "Target",
        "Datetime_utc",
        "Rating",
    ]

    def add_arguments(self, parser):
        parser.add_argument("file", type=str, help="Pattern for CSV file(s) to load")

    def handle(self, *_, **options):
        for file in glob(options["file"]):
            evaluations = Table.read(file, format="ascii.csv")

            # verify we have all the necessary fields
            if not set(evaluations.colnames).issuperset(set(self.required_fields)):
                self.stderr.write(
                    self.style.ERROR(
                        f"File must contain fields: {", ".join(self.required_fields)}"
                    )
                )
                return

            # turn each row into a database entry
            for evaluation in evaluations:
                # first, check that we know the target
                target_id = evaluation["Target"]
                try:
                    target = models.Target.objects.get(name=target_id)
                except:
                    self.stderr.write(
                        self.style.ERROR(f"Target ID: {target_id} not found")
                    )
                    return
                # find the referenced SpectrumRawData object
                date = datetime.fromisoformat(evaluation["Datetime_utc"]).astimezone(
                    timezone.utc
                )
                try:
                    spectrum = models.SpectrumRawData.objects.get(
                        target_id=target.id, datetime_utc=date
                    )
                except:
                    self.stderr.write(
                        self.style.ERROR(
                            f"Cannot find spectrum with target id {target.name} and datetime {date}"
                        )
                    )
                    return
                se = models.SpectrumEvaluation(
                    target=target,
                    spectrum=spectrum,
                    quality=float(evaluation["Rating"]),
                    comment="",
                )
                se.save()
            self.stdout.write(
                self.style.SUCCESS(
                    f"Added {len(evaluations)} spectrum evaluations from {file}"
                )
            )
