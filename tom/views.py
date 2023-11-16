from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views import generic

from .models import Target, Observatory

class IndexView(generic.ListView):
    template_name="tom/index.html"
    def get_queryset(self):
        return Target.objects.all()[:5]

class TargetView(generic.DetailView):
    model = Target
    template_name = "tom/target.html"

class ObservatoryView(generic.DetailView):
    model = Observatory
    template_name = "tom/observatory.html"
