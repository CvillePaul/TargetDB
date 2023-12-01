from django.contrib import admin

from .models import *

class TargetInline(admin.TabularInline):
    model = Target
    extra = 0

class ScienceTargetInline(admin.TabularInline):
    model = ScienceTarget
    extra = 0


class CalibrationTargetInline(admin.TabularInline):
    model = CalibrationTarget  # ScienceTarget.calibrations.through
    extra = 0


class ObservingSessionInline(admin.TabularInline):
    model = ObservingSession
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


class ScienceTargetAdmin(admin.ModelAdmin):
    fieldsets = [
        ("IDs", {"fields": ["local_id"]}),
        (None, {"fields": ["source", "magnitude"]}),
        (
            "Coordinates (J2000)",
            {
                "fields": ["ra", "dec", "pmra", "pmdec", "distance"],
                "classes": ["collapse"],
            },
        ),
    ]
    inlines = [CalibrationTargetInline, ScienceResultInline]
    list_filter = ["source"]


admin.site.register(ScienceTarget, ScienceTargetAdmin)
admin.site.register(CalibrationTarget)

class TargetListAdmin(admin.ModelAdmin):
    # inlines = [TargetInline]
    pass

admin.site.register(TargetList, TargetListAdmin)

class ObservatoryAdmin(admin.ModelAdmin):
    inlines = [ObservingSessionInline]


admin.site.register(Observatory, ObservatoryAdmin)

admin.site.register(ObservationPurpose)


admin.site.register(ObservingProgram)
admin.site.register(ObservingSession)
admin.site.register(SpeckleRawData)
admin.site.register(SpectrumRawData)


class ScienceResultAdmin(admin.ModelAdmin):
    inlines = [ScienceTargetInline]
    extra = 0


admin.site.register(ScienceResult)
