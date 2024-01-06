from astropy.coordinates import SkyCoord
from astropy.table import Table, join
from astropy.time import Time
import astropy.units as u
from astroquery.gaia import Gaia
from astroquery.mast import Catalogs
from django.core.management.base import BaseCommand
import numpy as np
from tom import models


class Command(BaseCommand):
    help = "Loads targets of all types from file, augmenting with online catalog data"
    required_fields = ['ID', 'ID Type', 'Target Type', 'Source']

    def add_arguments(self, parser):
        parser.add_argument(
            "file",
            type=str,
            default="Targets.csv",
            help="File containing targets.  Required fields: ID, ID Type, Target Type, Source",
        )

    def handle(self, *_, **options) -> None:
        target_list = Table.read(options["file"], format="ascii.csv", converters={"*": str})

        if not set(target_list.colnames).issuperset(set(self.required_fields)):
            self.stderr.write(
                self.style.ERROR(f"File must contain fields: {", ".join(self.required_fields)}")
            )
            return

        non_tess = target_list[target_list["ID Type"] != "TESS TIC"]
        if len(non_tess) > 0:
            self.stderr.write(
                self.style.ERROR("Only TESS TIC targets currently handled")
            )
            return

        # retrieve all objects by TIC ID from the TIC catalog, which (among other things) gives us the GAIA ID
        # TIC fields: https://mast.stsci.edu/api/v0/_t_i_cfields.html
        tic_table = Catalogs.query_criteria(catalog="Tic", ID=target_list["ID"])[["ID", "GAIA"]]

        if len(tic_table) != len(target_list):
            self.stderr.write(
                self.style.ERROR(
                    f"Tic query returned {len(tic_table)} instead of {len(target_list)} entries"
                )
            )
            return
        target_list = join(target_list, tic_table, keys_left="ID", keys_right="ID")

        # retrieve all objects by their associated GAIA IDs
        # GAIA fields: https://gea.esac.esa.int/archive/documentation/GDR2/Gaia_archive/chap_datamodel/sec_dm_main_tables/ssec_dm_gaia_source.html
        job = Gaia.launch_job(
            "select SOURCE_ID, REF_EPOCH, RA, DEC, PARALLAX, PMRA, PMDEC, phot_g_mean_mag from gaiadr2.gaia_source "
            "where SOURCE_ID IN (" + ",".join(target_list["GAIA"].data) + ") "
        )
        gaia_table = job.get_results()

        if len(gaia_table) != len(target_list):
            self.stderr.write(
                self.style.ERROR(
                    f"Tic query returned {len(gaia_table)} instead of {len(target_list)} entries"
                )
            )
            return

        # some of the results are missing proper motion & parallax - fill the missing values with defaults
        gaia_table["PMRA"] = gaia_table["PMRA"].filled(0)
        gaia_table["PMDEC"] = gaia_table["PMDEC"].filled(0)
        gaia_table["PARALLAX"] = gaia_table["PARALLAX"].filled(1e-3)

        # make a string version of the int64 source id so we can join this table against the tic table
        gaia_table["gaia source id"] = [str(id) for id in gaia_table["SOURCE_ID"]]

        # merge the gaia data into the table we've been building
        target_list = join(
            target_list, gaia_table, keys_left="GAIA", keys_right="gaia source id"
        )

        # define a distance column based on gaia parallax
        target_list["Distance"] = 1 / np.abs(target_list["PARALLAX"]) * u.parsec * u.mas

        # make a SkyCoord object for the RA/DEC of all the objects.
        # the SkyCoord object handles proper motion nicely, so PMRA and PMDEC are in there too
        gaia_coords = SkyCoord(
            target_list["RA"],
            target_list["DEC"],
            distance=target_list["Distance"],
            pm_ra_cosdec=target_list["PMRA"],
            pm_dec=target_list["PMDEC"],
            frame="icrs",
            obstime=Time(target_list["REF_EPOCH"], format="jyear", scale="tdb"),
        )

        # apply proper motion back to J2000
        j2000_coords = gaia_coords.apply_space_motion(
            Time(2000.0, format="jyear", scale="tdb")
        )
        target_list["RA2000"] = j2000_coords.ra
        target_list["Dec2000"] = j2000_coords.dec

        gaia_id_type = models.TargetIdType.objects.get(id_type="Gaia DR2")
        #write to the database
        for row in target_list:
            match row["Target Type"]:
                case "Target":
                    target = models.Target()
                case "Science":
                    target = models.ScienceTarget()
                case "Calibration":
                    target = models.CalibrationTarget()
                case _:
                    self.stderr.write(self.style.ERROR(f"Unknown target type {row["Target Type"]}"))
            target.local_id=f"TIC {row["ID_1"]}"
            target.source=row["Source"]
            target.ra = row["RA2000"]
            target.dec=row["Dec2000"]
            target.pmra=row["PMRA"]
            target.pmdec=row["PMDEC"]
            target.distance=row["Distance"]
            target.magnitude=row["phot_g_mean_mag"]
            target.save()
            target_identifier = models.TargetIdentifier(target=target, id_type=gaia_id_type, identifier=row["SOURCE_ID"])
            target_identifier.save()

        self.stdout.write(self.style.SUCCESS(f"Wrote {len(target_list)} targets"))
