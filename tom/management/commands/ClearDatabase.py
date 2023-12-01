from django.core.management.base import BaseCommand, CommandError
import inspect

# from tom.models import *
import tom.models as model_objects


class Command(BaseCommand):
    help = "Remove all entries from database, leaving only empty tables"

    def handle(self, *args, **options):
        for name, obj in inspect.getmembers(model_objects, inspect.isclass):
            if "Meta" in [x for x, _ in inspect.getmembers(obj, inspect.isclass)]:
                if "abstract" in [x for x, _ in inspect.getmembers(obj.Meta)]:
                    pass
            # can't figure out how to get the value of obj.Meta.abstract so these classes can be skipped
            # shitty workaround
            if name == "RawData":
                continue
            self.stdout.write(f"Deleting {name} rows...", ending="")
            try:
                obj.objects.all().delete()
                self.stdout.write(self.style.SUCCESS(f"Done."))
            except:
                self.stdout.write(self.style.ERROR(f"Error"))
