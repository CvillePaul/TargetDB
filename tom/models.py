from datetime import datetime
from astropy.coordinates import SkyCoord
import astropy.units as u
from django.db import models


class Person(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.CharField(max_length=100)
    affiliation = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class TargetIdType(models.Model):
    id_type = models.CharField(max_length=100, unique=True)
    comment = models.CharField(max_length=200, blank=True)


class Target(models.Model):
    local_id = models.CharField(max_length=100, unique=True)
    source = models.CharField(
        max_length=100, help_text="How target was identified/discovered", blank=True
    )
    ra = models.FloatField(verbose_name="RA (deg)")
    dec = models.FloatField(verbose_name="Dec (deg)")
    pmra = models.FloatField(verbose_name="PM RA (mas/yr)", default=0)
    pmdec = models.FloatField(verbose_name="PM Dec (mas/yr)", default=0)
    distance = models.FloatField(verbose_name="Distance (pc)", default=0)
    magnitude = models.FloatField()

    def __str__(self):
        return self.local_id

    def isCloseTo(self, coord: SkyCoord) -> bool:
        coord = SkyCoord(
            ra=self.ra * u.deg,
            dec=self.dec * u.deg,
            pm_ra_cosdec=self.pmra * u.mas / u.yr,
            pm_dec=self.pmdec * u.mas / u.yr,
            frame="icrs",
        )
        return coord.separation(coord) < 10 * u.arcsec


class TargetIdentifier(models.Model):
    target = models.ForeignKey(Target, on_delete=models.CASCADE)
    id_type = models.ForeignKey(TargetIdType, on_delete=models.CASCADE)
    identifier = models.CharField(max_length=100)


class CalibrationTarget(Target):
    ...


class ScienceTarget(Target):
    calibrations = models.ManyToManyField(CalibrationTarget)


class TargetList(models.Model):
    name = models.CharField(max_length=200, unique=True)
    created = models.DateTimeField(auto_now_add=True)
    description = models.CharField(max_length=400)
    targets = models.ManyToManyField(Target)

    def __str__(self):
        return f"{self.name} (created {self.created:%Y-%m-%d %H:%M:%S} UTC)"


class Observatory(models.Model):
    nickname = models.CharField(max_length=15)
    name = models.CharField(max_length=100)
    iau_code = models.CharField(max_length=10)

    def __str__(self):
        return self.nickname


class ObservationPurpose(models.Model):
    purpose = models.CharField(max_length=100)

    def __str__(self):
        return self.purpose


class ObservingProgram(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name

    def unknownProgram() -> str:
        return "Unknown"


class ObservingSession(models.Model):
    observingprogram = models.ForeignKey(ObservingProgram, on_delete=models.CASCADE)
    observatory = models.ForeignKey(Observatory, on_delete=models.CASCADE)
    utc_date = models.DateField()
    equipment = models.CharField(
        max_length=200,
        help_text=f"Format: <telescope>+<instrument>",
    )
    purpose = models.ForeignKey(ObservationPurpose, on_delete=models.CASCADE)
    observers = models.ManyToManyField(Person)

    def __str__(self):
        return f"{self.purpose} of {self.target} on {self.utc_date} @ {self.observatory.nickname} "

    def makeEquipmentString(telescope: str, instrument: str) -> str:
        return f"{telescope}+{instrument}"


class RawData(models.Model):
    target = models.ForeignKey(Target, on_delete=models.CASCADE)
    observingsession = models.ForeignKey(ObservingSession, on_delete=models.CASCADE)
    datetime_utc = models.DateTimeField(default=datetime.fromisoformat("1970-01-01"))
    uri = models.CharField(max_length=200)

    def __str__(self):
        return self.uri

    class Meta:
        abstract = True


class SpeckleRawData(RawData):
    gain = models.PositiveIntegerField(default=0)
    exposure_time_ms = models.PositiveIntegerField(default=0)
    num_sequences = models.PositiveIntegerField(default=0)
    channels = models.CharField(max_length=100)


class SpectrumRawData(RawData):
    fiber = models.CharField(max_length=20, default="")
    cross_disperser = models.CharField(max_length=100, default="")
    arm = models.CharField(max_length=30, default="")
    exposure_time = models.FloatField(default=0)


# class PhotometryRawData(RawData):
#     pass


# class OtherRawData(RawData):
#     description = models.CharField(max_length=200)


class ScienceResult(models.Model):
    target = models.ForeignKey(Target, on_delete=models.CASCADE)
    type = models.CharField(max_length=30)
    author = models.CharField(max_length=200, default="")
    uri = models.CharField(max_length=200)

    def __str__(self):
        return self.uri
