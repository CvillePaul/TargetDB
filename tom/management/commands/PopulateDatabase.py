from django.core.management.base import BaseCommand, CommandError
from tom.models import *
from tom.TargetImporter import TargetImporter


class Command(BaseCommand):
    help = "Loads a bunch of standard items into a presumably empty database"

    def add_arguments(self, parser):
        parser.add_argument(
            "--entities",
            action="store_true",
            help="Load things like people, observatories, observation types, etc.",
        )

        parser.add_argument(
            "--targets",
            action="store_true",
            help="Load targets from lists of ids",
        )

    def handle(self, *args, **options):
        if options["entities"]:
            ObservationPurpose(purpose="Photometry").save()
            ObservationPurpose(purpose="Spectroscopy").save()
            ObservationPurpose(purpose="Speckle Imaging").save()

            Observatory(
                nickname="APO", name="Apache Point Observatory", iau_code="705"
            ).save()
            Observatory(
                nickname="LBT", name="Large Binocular Telescope", iau_code="G83"
            ).save()
            Observatory(nickname="Fan", name="Fan Mountain", iau_code="I18").save()

            Person(
                first_name="Jimmy",
                last_name="Davidson",
                email="jimmy@virginia.edu",
                affiliation="UVA",
            ).save()
            Person(
                first_name="Steve",
                last_name="Majewski",
                email="srm4n@virginia.edu",
                affiliation="UVA",
            ).save()
            Person(
                first_name="Paul",
                last_name="McKee",
                email="pmm3w@virginia.edu",
                affiliation="UVA",
            ).save()

            ObservingProgram(name="QuadEB").save()

        if options["targets"]:
            num_targets = TargetImporter.process_target_file(
                "../../Files/Master Object List.ecsv", False
            )
            self.stdout.write(self.style.SUCCESS(f"Loaded {num_targets} targets"))
