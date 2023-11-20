from django.contrib import admin

from .models import *

class TargetInline(admin.TabularInline):
    model = Target
    extra = 0

class ObservationInline(admin.TabularInline):
    model = Observation
    extra = 0

class RawDataInline(admin.TabularInline):
    model = RawData
    extra = 0

class SpeckleRawDataInline(admin.TabularInline):
    model = SpeckleRawData
    extra = 0

class ScienceResultInline(admin.TabularInline):
    model = ScienceResult
    extra = 0

admin.site.register(Person)

class TargetAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {"fields": ["local_id", "tic_id", "gaia_id"]}),
        (None, {"fields": ["magnitude"]}),
        ("Coordinates (J2000)", {"fields": ["ra", "dec", "pmra", "pmdec", "distance"], "classes": ["collapse"]}),
        ("Ephemeredes", {"fields": [], "classes": ["collapse"]}),
    ]
    inlines = [ObservationInline, ScienceResultInline]
    list_filter = ["source"]
    extra = 0

admin.site.register(Target, TargetAdmin)

class ObservatoryAdmin(admin.ModelAdmin):
    inlines = [ObservationInline]
admin.site.register(Observatory, ObservatoryAdmin)

admin.site.register(ObservationPurpose)

class ObservationAdmin(admin.ModelAdmin):
    inlines = [SpeckleRawDataInline]
admin.site.register(Observation, ObservationAdmin)

admin.site.register(SpeckleRawData)
admin.site.register(SpectrumRawData)
admin.site.register(PhotometryRawData)
admin.site.register(OtherRawData)

class ScienceResultAdmin(admin.ModelAdmin):
    inlines = [TargetInline]
    extra = 0
admin.site.register(ScienceResult)
