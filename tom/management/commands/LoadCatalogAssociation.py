from glob import glob
from astropy.table import Table
from django.core.management.base import BaseCommand
from tom import models


class Command(BaseCommand):
    help = "Stores connections between Target objects and objects in astronomical catalogs."
    required_fields = ["Local ID", "Catalog", "Catalog ID", "Association"]


    def add_arguments(self, parser):
        parser.add_argument("file", type=str, help="Pattern for CSV file(s) to load")

    def handle(self, *_, **options) -> None:
        for file in glob(options["file"]):
            associations = Table.read(file, format="ascii.csv", converters={"*": str})

            if not set(associations.colnames).issuperset(set(self.required_fields)):
                self.stderr.write(
                    self.style.ERROR(f"File {file} must contain fields: {", ".join(self.required_fields)}")
                )
                return

            num_created, num_updated = 0, 0
            for association in associations:
                target = models.Target.objects.get(local_id=association["Local ID"])
                _, created = models.CatalogAssociation.objects.update_or_create(
                    target=target,
                    catalog=association["Catalog"],
                    catalog_id=association["Catalog ID"],
                    association=association["Association"],
                )
                if created:
                    num_created += 1
                else:
                    num_updated += 1

            self.stderr.write(
                self.style.SUCCESS(f"Created {num_created} and updated {num_updated} associations from {file}")
            )
