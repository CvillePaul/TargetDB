from django.core.management.base import BaseCommand
from tom import models

class Command(BaseCommand):
    help = "Loads a bunch of standard items into a presumably empty database"

    def add_arguments(self, parser):
        parser.add_argument("filename", type=str)

    def handle(self, *args, **options):
        file = open(options["filename"], "r")
        listname = file.readline().rstrip() #kill EOL chars
        local_ids = file.readlines()

        targets = []
        errors = 0
        for local_id in local_ids:
            try:
                targets.append(models.Target.objects.get(local_id=local_id.strip()))
            except:
                self.stderr.write(self.style.ERROR(f"Cannot locate target {local_id}, {len(local_id)}"))
                errors += 1
        if errors > 0:
            self.stderr.write(self.style.ERROR(f"Quitting with {errors} errors"))
            return

        targetlist = models.TargetList(name=listname)
        targetlist.save()

        for target in targets:
            targetlist.targets.add(target)
        targetlist.save()

        self.stdout.write(self.style.SUCCESS(f"Created list {listname} with {len(targets)} members"))
