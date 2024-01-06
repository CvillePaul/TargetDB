from datetime import datetime, timezone
from astropy.table import Table
import astropy.units as u
from django.core.management.base import BaseCommand
from tom import models


class Command(BaseCommand):
    help = "Loads speckle observations from the specified CSV file"
    required_fields = [
        "Observing Program",
        "Observatory",
        "Equipment",
        "Target",
        "DateTimeUTC",
        "Fiber",
        "Arm",
        "Cross Disperser",
        "Exposure Time",
        "File",
    ]
        # ("Observing Program", str),
        # ("Observatory", str),
        # ("Equipment", str),
        # ("Target", str),
        # ("DateTimeUTC", str),
        # ("Fiber", str),
        # ("Arm", str),
        # ("Cross Disperser", str),
        # ("Exposure Time", float),
        # ("File", str),

    def add_arguments(self, parser):
        parser.add_argument("file", type=str, help="CSV file to load")

    def handle(self, *_, **options):
        observations = Table.read(options["file"], format="ascii.csv")

        # verify we have all the necessary fields
        if not set(observations.colnames).issuperset(set(self.required_fields)):
            self.stderr.write(
                self.style.ERROR(
                    f"File must contain fields: {", ".join(self.required_fields)}"
                )
            )
            return

        # turn each row into a database entry
        for observation in observations:
            # first, check that we know the target
            target_id = observation["Target"]
            try:
                target = models.Target.objects.get(local_id=target_id)
            except:
                self.stderr.write(self.style.ERROR(f"Target ID: {target_id} not found"))
                return
            # now gather data for the observing session
            date = datetime.fromisoformat(observation["DateTimeUTC"]).astimezone(
                timezone.utc
            )
            observing_program = models.ObservingProgram.objects.get(
                name=observation["Observing Program"]
            )
            observatory = models.Observatory.objects.get(
                nickname=observation["Observatory"]
            )
            equipment = observation["Equipment"]
            try:
                observing_session = models.ObservingSession.objects.get(
                    observingprogram=observing_program,
                    observatory=observatory,
                    equipment=equipment,
                    utc_date=date.date().isoformat(),
                )
            except:
                #TODO: should only catch DoesNotExist exceptions
                observing_session = models.ObservingSession(
                    observingprogram=observing_program,
                    observatory=observatory,
                    equipment=equipment,
                    utc_date=date.date().isoformat(),
                    purpose=models.ObservationPurpose.objects.get(
                        purpose="Speckle Imaging"
                    ),
                )
                observing_session.save()
            srd = models.SpectrumRawData()
            srd.target = target
            srd.datetime_utc = date
            srd.observingsession = observing_session
            # handle rest of the fields
            srd.fiber = observation["Fiber"]
            srd.arm = observation["Arm"]
            srd.cross_disperser = observation["Cross Disperser"]
            srd.exposure_time = observation["Exposure Time"]
            srd.uri = observation["File"]
            srd.save()
            self.stdout.write(
                self.style.SUCCESS(
                    f"{target.local_id} at {srd.datetime_utc} on {srd.cross_disperser}"
                )
            )
