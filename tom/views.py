from django.shortcuts import get_object_or_404, render
from django.views import generic

from .models import *

class IndexView(generic.ListView):
    template_name="tom/index.html"
    def get_queryset(self):
        return Target.objects.all()[:5]

def TargetView(request, pk):
    target = get_object_or_404(Target, pk=pk)
    observations = target.observation_set.all()
    scienceresults = target.scienceresult_set.all()
    specklerawdata = SpeckleRawData.objects.filter(observation__target__local_id=target.local_id)
    context = {"target": target, "observations": observations, "specklerawdata": specklerawdata, "scienceresults": scienceresults}
    return render(request, "tom/target.html", context)

class ObservatoryView(generic.DetailView):
    model = Observatory
    template_name = "tom/observatory.html"

class ObservationView(generic.DetailView):
    model = Observation
    template_name = "tom/observation.html"

class PersonView(generic.DetailView):
    model = Person
    template_name = "tom/person.html"

# def StatusView(request):
#     targets =