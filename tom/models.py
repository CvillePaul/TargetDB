from django.db import models

class Person(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.CharField(max_length=100)
    affiliation = models.CharField(max_length=100)

class Target(models.Model):
    local_id = models.CharField(max_length=100, unique=True)
    tic_id = models.CharField(max_length=30)
    gaia_id = models.CharField(max_length=30)
    ra = models.FloatField("RA(2000) (deg)")
    dec = models.FloatField("Dec(2000) (deg)")
    pmra = models.FloatField("PM RA (mas/yr)")
    pmdec = models.FloatField("PM Dec (mas/yr)")
    distance = models.FloatField("Distance (pc)")
    def __str__(self):
        return self.local_id

class Observatory(models.Model):
    nickname = models.CharField(max_length=15)
    name = models.CharField(max_length=100)
    iau_code = models.CharField(max_length=10)
    def __str__(self):
        return self.name

class Observation(models.Model):
    target = models.ForeignKey(Target, on_delete=models.CASCADE)
    observatory = models.ForeignKey(Observatory, on_delete=models.CASCADE)
    utc_date = models.DateField()
    equipment = models.CharField(max_length=100)

class Observer(models.Model):
    observation = models.ForeignKey(Observation, on_delete=models.CASCADE)
    person = models.ForeignKey(Person, on_delete=models.CASCADE)

class RawData(models.Model):
    observation = models.ForeignKey(Observation, on_delete=models.CASCADE)
    uri = models.CharField(max_length=200)
    size = models.IntegerField()
    def __str__(self):
        return self.uri
    class Meta:
        abstract = True

class SpeckleRawData(RawData):
    gain = models.PositiveIntegerField()
    exposure_time_ms = models.PositiveIntegerField()
    num_sequences = models.PositiveIntegerField()

class SpectrumRawData(RawData):
    pass

class PhotometryRawData(RawData):
    pass

class OtherRawData(RawData):
    description = models.CharField(max_length=200)

class ScienceResult(models.Model):
    target = models.ForeignKey(Target, on_delete=models.CASCADE)
    type = models.CharField(max_length=20)
    author = models.CharField(max_length=200, default="")
    uri = models.CharField(max_length=200)
    def __str__(self):
        return self.uri