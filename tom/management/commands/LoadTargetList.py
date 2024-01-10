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
            local_ids = file.readlines()  # TODO: should use id type/id pair here and below

            targets = []
            errors = 0
            for local_id in local_ids:
                try:
                    targets.append(models.Target.objects.get(local_id=local_id.strip()))
                except:
                    self.stderr.write(
                        self.style.ERROR(
                            f"Cannot locate target {local_id}, {len(local_id)}"
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
