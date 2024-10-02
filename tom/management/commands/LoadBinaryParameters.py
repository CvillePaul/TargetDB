from glob import glob
import os
from astropy.table import Table
from django.core.management.base import BaseCommand
from tom import models


class Command(BaseCommand):
    help = "Loads data such as period, duration, depth of binary components of a target"
    required_fields = ["Local ID", "Member", "Period", "T0", "Duration", "Depth"]

    def add_arguments(self, parser):
        parser.add_argument("file", type=str, help="Pattern for CSV file(s) to load")

    def handle(self, *_, **options) -> None:
        for file in glob(options["file"]):
            parameters = Table.read(file, format="ascii.csv")

            if not set(parameters.colnames).issuperset(set(self.required_fields)):
                self.stderr.write(
                    self.style.ERROR(f"File {file} must contain fields: {", ".join(self.required_fields)}")
                )
                return

            num_created, num_updated = 0, 0
            for parameter in parameters:
                # get the column(s) that make a row unique
                try:
                    name = str(parameter["Local ID"])
                    target = models.Target.objects.get(name=name)
                except Exception as e:
                    self.stderr.write(
                        self.style.ERROR(f"Cannot find target {name} from file {file}")
                    )
                    return
                t0 = parameter["T0"] + 2457000 # adjust to BJD
                period = parameter["Period"] / 3600 # convert from hours to seconds
                if (duration := parameter.get("Duration")) is None:
                    duration = 0 # default value
                if (depth := parameter.get("Depth")) is None:
                    depth = 0 # default value

                #load into the database
                _, created = models.BinaryParameters.objects.update_or_create(
                    target=target,
                    system=parameter["System"],
                    member=parameter["Member"],
                    t0=t0,
                    period=period,
                    duration=duration,
                    depth=depth,
                )
                if created:
                    num_created += 1
                else:
                    num_updated += 1

            self.stderr.write(
                self.style.SUCCESS(f"Created {num_created} and updated {num_updated} binary parameter entries from {file}")
            )
