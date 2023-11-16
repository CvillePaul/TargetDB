from django.contrib import admin

from .models import *

class ObservationInline(admin.TabularInline):
    model = Observation
    extra = 0

class ObserverInline(admin.TabularInline):
    model = Observer
    extra = 0

class RawDataInline(admin.TabularInline):
    model = RawData
    extra = 0

admin.site.register(Person)

class TargetAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {"fields": ["local_id", "tic_id", "gaia_id"]}),
        ("Astrometry (J2000)", {"fields": ["ra", "dec", "pmra", "pmdec", "distance"]})
    ]
    inlines = [ObservationInline]
    extra = 0

admin.site.register(Target, TargetAdmin)

class ObservatoryAdmin(admin.ModelAdmin):
    inlines = [ObservationInline]
    extra = 0
admin.site.register(Observatory, ObservatoryAdmin)

admin.site.register(ObservationPurpose)

class ObservationAdmin(admin.ModelAdmin):
    inlines = [ObserverInline]
    extra = 0
admin.site.register(Observation, ObservationAdmin)

admin.site.register(Observer)
admin.site.register(SpeckleRawData)
admin.site.register(SpectrumRawData)
admin.site.register(PhotometryRawData)
admin.site.register(OtherRawData)
admin.site.register(ScienceResult)
