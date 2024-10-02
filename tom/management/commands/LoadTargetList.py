from glob import glob
from django.core.management.base import BaseCommand
from tom import models


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument(
            "filename", type=str, help="Source of target list(s).  Wildcards OK"
        )

    def handle(self, *args, **options):
        for filename in glob(options["filename"]):
            file = open(filename, "r")
            listname = file.readline().rstrip()  # kill EOL chars
            description = file.readline().rstrip()
            names = file.readlines()  # TODO: should use id type/id pair here and below

            targets = []
            errors = 0
            for name in names:
                try:
                    targets.append(models.Target.objects.get(name=name.strip()))
                except:
                    self.stderr.write(
                        self.style.ERROR(
                            f"Cannot locate target {name}, {len(name)}"
                        )
                    )
                    errors += 1
            if errors > 0:
                self.stderr.write(self.style.ERROR(f"Quitting with {errors} errors"))
                return

            targetlist = models.TargetList(name=listname, description=description)
            targetlist.save()

            for target in targets:
                targetlist.targets.add(target)
            targetlist.save()

            self.stdout.write(
                self.style.SUCCESS(f"Created list {listname} with {len(targets)} members")
            )
