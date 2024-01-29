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

        tess_id_name = "TESS TICv8"
        gaia2_id_name = "GAIA DR2"
        gaia3_id_name = "GAIA DR3"
        target_loaders = {
            tess_id_name: self.load_tess_targets,
            gaia2_id_name: self.load_gaia2_targets,
            gaia3_id_name: self.load_gaia3_targets,
        }

        grouped_targets = target_list.group_by("ID Type")
        for id_type, targets in zip(grouped_targets.groups.keys, grouped_targets.groups):
            try:
                target_loaders[id_type](targets)
            except:
                self.stderr.write(
                    self.style.ERROR(f"Unknown target id type: {id_type}")
                )
                return

        # retrieve all objects by TIC ID from the TIC catalog, which (among other things) gives us the GAIA ID
        # TIC fields: https://mast.stsci.edu/api/v0/_t_i_cfields.html
        tic_table = Catalogs.query_criteria(catalog="Tic", ID=target_list["ID"])
        tic_table.rename_column("ID", "Tess_TICv8")

        if len(tic_table) != len(target_list):
            self.stderr.write(
                self.style.ERROR(
                    f"Tic query returned {len(tic_table)} instead of {len(target_list)} entries"
                )
            )
            return
        target_list = join(target_list, tic_table, keys_left="ID", keys_right="ID")


        # merge the gaia data into the table we've been building
        target_list = join(
            target_list, gaia_table, keys_left="GAIA", keys_right="gaia source id"
        )

        # define a distance column based on gaia parallax
        target_list["Distance"] = u.mas / np.abs(target_list["PARALLAX"]) * 1000 # convert from kiloparsecs to parsecs

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
        tess_id_type = models.TargetIdType.objects.get(id_type="TESS TICv8")
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
            tess_identifier = models.TargetIdentifier(target=target, id_type=tess_id_type, identifier=row["Tess_TICv8"])
            tess_identifier.save()
            gaia_identifier = models.TargetIdentifier(target=target, id_type=gaia_id_type, identifier=row["SOURCE_ID"])
            gaia_identifier.save()


        self.stdout.write(self.style.SUCCESS(f"Wrote {len(target_list)} targets"))

    def load_tess_targets():
        ...

    def load_gaia2_targets(self, targets):
        self.load_gaia_targets("gaiadr2.gaia_source", targets)

    def load_gaia3_targets(self, targets):
        self.load_gaia_targets("gaiadr3.gaia_source", targets)

    def load_gaia_targets(self, table_name, targets):
        # retrieve all objects by their associated GAIA IDs
        # GAIA fields: https://gea.esac.esa.int/archive/documentation/GDR2/Gaia_archive/chap_datamodel/sec_dm_main_tables/ssec_dm_gaia_source.html
        job = Gaia.launch_job(
            f"select SOURCE_ID, REF_EPOCH, RA, DEC, PARALLAX, PMRA, PMDEC, phot_g_mean_mag from {table_name} "
            "where SOURCE_ID IN (" + ",".join(targets["ID"].data) + ") "
        )
        gaia_table = job.get_results()

        if len(gaia_table) != len(targets):
            self.stderr.write(
                self.style.ERROR(
                    f"Tic query returned {len(gaia_table)} instead of {len(targets)} entries"
                )
            )
            return

        # some of the results are missing proper motion & parallax - fill the missing values with defaults
        gaia_table["PMRA"] = gaia_table["PMRA"].filled(0)
        gaia_table["PMDEC"] = gaia_table["PMDEC"].filled(0)
        gaia_table["PARALLAX"] = gaia_table["PARALLAX"].filled(1e-3)

        # make a string version of the int64 source id so we can join this table against the tic table
        gaia_table["gaia source id"] = [str(id) for id in gaia_table["SOURCE_ID"]]

