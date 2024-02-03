from glob import glob
import os
from astropy.table import Table
from django.core.management.base import BaseCommand
from tom import models


class Command(BaseCommand):
    help = "Loads data such as period, duration, depth of binary components of a target"
    required_fields = ["Local ID", "Member", "Period", "T0 Primary", "T0 Secondary", "Duration Primary", "Duration Secondary", "Depth Primary", "Depth Secondary"]

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
                #assume these are all TIC IDs, if only a number prepend TIC to it
                try:
                    local_id = str(parameter["Local ID"])
                    if not "TIC " in local_id:
                        local_id = f"TIC {local_id}"
                    target = models.Target.objects.get(local_id=local_id)
                except Exception as e:
                    self.stderr.write(
                        self.style.ERROR(f"Cannot find target {local_id} from file {file}")
                    )
                    return
                member = parameter["Member"]
                vals = {
                    key.lower().replace(" ", "_"): val
                    for key, val in zip(parameter.keys(), parameter.values())
                    if val != "masked"
                }
                vals["type"] = "Binary Parameters"
                vals["uri"] = os.path.basename(file)
                #remove the unique columns retrieved above
                del vals["local_id"]
                del vals["member"]

                #load into the database
                _, created = models.BinaryParameters.objects.update_or_create(
                    target=target,
                    member=member,
                    defaults=vals,
                )
                if created:
                    num_created += 1
                else:
                    num_updated += 1

            self.stderr.write(
                self.style.SUCCESS(f"Created {num_created} and updated {num_updated} binary parameter entries from {file}")
            )
