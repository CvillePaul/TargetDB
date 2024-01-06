from django.core.management.base import BaseCommand, CommandError
import inspect

from tom import models

class Command(BaseCommand):
    help = "Remove all entries from database, leaving only empty tables"

    def handle(self, *args, **options):
        models.ScienceResult.objects.all().delete()
        models.SpeckleRawData.objects.all().delete()
        models.SpectrumRawData.objects.all().delete()
        # models.PhotometryRawData.objects.all().delete()
        # models.OtherRawData.objects.all().delete()
        models.ObservingSession.objects.all().delete()
        models.ObservingProgram.objects.all().delete()
        models.ObservationPurpose.objects.all().delete()
        models.Observatory.objects.all().delete()
        models.TargetList.objects.all().delete()
        models.ScienceTarget.objects.all().delete()
        models.CalibrationTarget.objects.all().delete()
        models.TargetIdentifier.objects.all().delete()
        models.Target.objects.all().delete()
        models.TargetIdType.objects.all().delete()
        models.Person.objects.all().delete()

        # for name, obj in inspect.getmembers(model_objects, inspect.isclass):
        #     if "Meta" in [x for x, _ in inspect.getmembers(obj, inspect.isclass)]:
        #         if "abstract" in [x for x, _ in inspect.getmembers(obj.Meta)]:
        #             pass
        #     # can't figure out how to get the value of obj.Meta.abstract so these classes can be skipped
        #     # shitty workaround
        #     if name in ["RawData", "SkyCoord", "datetime"]:
        #         continue
        #     self.stdout.write(f"Deleting {name} rows...", ending="")
        #     try:
        #         obj.objects.all().delete()
        #         self.stdout.write(self.style.SUCCESS(f"Done."))
        #     except:
        #         self.stdout.write(self.style.ERROR(f"Error"))

        self.stdout.write(self.style.SUCCESS("All database tables cleared"))
