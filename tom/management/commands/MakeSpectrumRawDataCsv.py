from datetime import datetime
from glob import glob
import os
from django.core.management.base import BaseCommand
from tom import models
from . import LoadSpectrumRawData
from astropy.io import fits
from astropy.table import Table
# class CsvContents:
#     def __init__(self, columns: list(str)):
#         self.columns = dict(map(lambda col: (col, CsvContents._sanitize_column_name(col)), columns))
#         self.__dict__ = dict(map(lambda x: (x, None), self.columns.values()))

#     def _sanitize_column_name(column_name: str) -> str:
#         return column_name.replace(" ", "_").lower()

#     def add_row(self, **data):
#         for column, value in data:
#             self.__dict__.set(column, value)

#     def csv_contents(self) -> str:


class Command(BaseCommand):
    help = "Parse a directory of LBT spectrum FITS files and create a csv summarizing them"

    def add_arguments(self, parser):
        parser.add_argument("infiles", type=str, help="Pattern of FITS file(s)")
        parser.add_argument("outfile", type=str, help="Name of CSV file to create")
        parser.add_argument("observing_program", type=str, help="Name of the observing program")

    def handle(self, *_, **options):
        filename = options["outfile"]
        if not filename.lower().endswith(".csv"):
            filename = filename + ".csv"
        observing_program = options["observing_program"]
        column_names = LoadSpectrumRawData.Command.required_fields
        measurements = Table(names=column_names, dtype=[str]*len(column_names))

        for file in glob(options["infiles"]):
            hdr = fits.open(file)[0].header
            observatory = hdr["TELESCOP"]
            equipment = models.ObservingSession.makeEquipmentString(hdr["TELESCOP"], hdr["INSTRUME"])
            target = hdr["OBJECT"]
            datetime_utc = f"{hdr["DATE-OBS"]}T{hdr["TIME-OBS"]}Z"
            fiber = hdr["FIBER"]
            arm = hdr["ARM"]
            cross_disperser = hdr["CROSDIS"]
            exposure_time = str(hdr["EXPTIME"])

            measurements.add_row({
                "Observing Program" : observing_program,
                "Observatory" : observatory,
                "Equipment" : equipment,
                "Target" : target,
                "DateTimeUTC" : datetime_utc,
                "Fiber" : fiber,
                "Arm" : arm,
                "Cross Disperser" : cross_disperser,
                "Exposure Time" : exposure_time,
                "File" : os.path.basename(file),
            })
        measurements.write(filename)
        self.stdout.write(self.style.SUCCESS(f"Wrote {len(measurements)} rows to {filename}"))
