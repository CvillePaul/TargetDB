from datetime import datetime
from glob import glob
from astropy.coordinates import SkyCoord
from astropy.io import fits
import astropy.units as u
from django.core.management.base import BaseCommand
from tom import models

class Command(BaseCommand):
    help = "Walks through pepsi*.fits files and creates SpectrumRawData entries from them"

    def add_arguments(self, parser):
        parser.add_argument("dir", type=str, help="Directory to find fits files")

    def handle(self, *_, **options):

        for file in glob(f"{options["dir"]}/pepsi*.bwl"):
            hdr = fits.open(file)[0].header
            srd = models.SpectrumRawData()

            # first, check that we know the target
            target_id = hdr["OBJECT"]
            try:
                target = models.Target.objects.get(local_id=target_id)
            except:
                self.stderr.write(self.style.ERROR(f"Target ID: {target_id} not found"))
                return
            # check that the listed coordinates are close to the ones we have
            spec_coord = SkyCoord(f"{hdr["RA2000"]} {hdr["DE2000"]}", unit=(u.hourangle, u.deg))
            if not target.isCloseTo(spec_coord):
                self.stderr.write(self.style.ERROR(f"Coordinates for target {target_id} of {spec_coord} are too far from database coordinates"))
                return
            srd.target = target
            # now gather data for the observing session
            date = datetime.fromisoformat(f"{hdr["DATE-OBS"]}")
            observatory = models.Observatory.objects.get(nickname=hdr["TELESCOP"])
            equipment = models.ObservingSession.makeEquipmentString(hdr["TELESCOP"], hdr["INSTRUME"])
            try:
                observing_session = models.ObservingSession.objects.get(observatory=observatory, equipment=equipment, utc_date=date)
            except:
                observing_program = models.ObservingProgram.objects.get(name=models.ObservingProgram.unknownProgram())
                observing_session = models.ObservingSession(
                    observing_program=observing_program,
                    observatory=observatory,
                    equipment=equipment,
                    utc_date=date,
                    purpose=models.ObservationPurpose.objects.get(purpose="Spectroscopy"),
                )
                observing_session.save()
            srd.observing_session = observing_session
            #handle rest of the fields
            srd.uri = file
            srd.fiber = hdr["FIBER"]
            srd.cross_disperser = hdr["CROSDIS"]
            srd.arm = hdr["ARM"]
            srd.exposure_time = hdr["EXPTIME"]
            srd.save()
            self.stdout.write(self.style.SUCCESS(f"{target.local_id} on {observing_session.utc_date} with {srd.arm} for {srd.exposure_time}"))
