from django.contrib import admin

from .models import *

class ObservationInline(admin.TabularInline):
    model = Observation

class ObserverInline(admin.TabularInline):
    model = Observer

class RawDataInline(admin.TabularInline):
    model = RawData

class TargetAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {"fields": ["local_id", "tic id", "gaia_id"]}),
        ("Astrometry", {"fields": ["ra", "dec", "pmra", "pmdec", "distance"]})
    ]
    inlines = [ObservationInline]

admin.site.register(Target, TargetAdmin)

admin.site.register(Observatory)

class ObservationAdmin(admin.ModelAdmin):
    inlines = [ObserverInline, RawDataInline]

admin.site.register(Observation, ObservationAdmin)

admin.site.register(SpeckleRawData)
admin.site.register(OtherRawData)
admin.site.register(ScienceResult)
