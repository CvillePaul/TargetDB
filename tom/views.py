from io import StringIO
import csv
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.views import generic

from .models import *
from .forms import *
from .TargetImporter import *


class IndexView(generic.ListView):
    template_name = "tom/index.html"

    def get_queryset(self):
        return Target.objects.all()[:5]


def TargetView(request, pk):
    target = get_object_or_404(ScienceTarget, pk=pk)
    observations = target.observation_set.all()
    scienceresults = target.scienceresult_set.all()
    specklerawdata = SpeckleRawData.objects.filter(
        observation__target__local_id=target.local_id
    )
    context = {
        "target": target,
        "observations": observations,
        "specklerawdata": specklerawdata,
        "scienceresults": scienceresults,
    }
    calibration_targets = target.calibrations
    if calibration_targets is not None:
        context["calibration_targets"] = calibration_targets.all()
    return render(request, "tom/target.html", context)


def ImportTargetsView(request):
    if request.method == "POST":
        form = ImportTargetsForm(request.POST, request.FILES)
        if form.is_valid():
            err_msg = TargetImporter.process_target_file(
                request.FILES["file"], form.cleaned_data["require_all"]
            )
            if err_msg == "":
                return HttpResponseRedirect("tom/import_targets_thanks")
            else:
                pass  # TODO: show error message to user
    else:
        form = ImportTargetsForm()
    return render(
        request,
        "tom/import_targets.html",
        {"form": form, "csv_columns": TargetImporter.csv_columns},
    )


class ObservatoryView(generic.DetailView):
    model = Observatory
    template_name = "tom/observatory.html"


class ObservationView(generic.DetailView):
    model = Observation
    template_name = "tom/observation.html"


class PersonView(generic.DetailView):
    model = Person
    template_name = "tom/person.html"
