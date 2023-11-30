from astropy import units as u
from astropy.table import QTable, join
from astropy.coordinates import SkyCoord
from astropy.time import Time
from astroquery.gaia import Gaia
from astroquery.mast import Catalogs
import numpy as np

from .models import *

class TargetImporter:

    catalogs = ["TESS TIC", "Gaia DR2"]
    target_types = ["Scientific", "Calibration", "Generic"]
    csv_columns = [
        ("Source", "Paper or other artefact that caused interest in this target"),
        ("ID", "Identifier that should be used to look up target information"),
        ("ID Type", f"Catalog to which ID belongs.  Allowed choices: {", ".join(catalogs)}"),
        ("Target Type", f"How the target should be used.  Allowed choices: {", ".join(target_types)}"),
        ]

    def process_target_file(file: string, require_all: bool) -> int:
        targets = QTable.read(file, format="ascii.ecsv")
        #TODO: verify all required columns are present

        #TODO: split table by ID Type, process each group separately
        targets.rename_column("ID", "TIC ID")

        tic_targets = TargetImporter.import_targets_by_tic(targets, require_all)

        for row in tic_targets:
            t = ScienceTarget(
                local_id = "TIC " + row["TIC ID"],
                source = row["Source"],
                ra = row["RA"].value,
                dec = row["Dec"].value,
                pmra = row["PMRA"].value,
                pmdec =  row["PMDEC"].value,
                distance = row["Distance"].value,
                magnitude = row["phot_g_mean_mag"].value,
            )
            t.save()

        return len(tic_targets)


    def import_targets_by_tic(targets_table: QTable, require_all: bool=False) -> QTable:
        # retrieve all objects by TIC ID from the TIC catalog, which (among other things) gives us the GAIA ID
        # TIC fields: https://mast.stsci.edu/api/v0/_t_i_cfields.html
        tic_table = Catalogs.query_criteria(catalog="Tic", ID=targets_table["TIC ID"])

        if require_all and len(tic_table) != len(targets_table):
            return None

        targets_table = join(targets_table, tic_table, keys_left="TIC ID", keys_right="ID")

        # retrieve all objects by their associated GAIA IDs
        # GAIA fields: https://gea.esac.esa.int/archive/documentation/GDR2/Gaia_archive/chap_datamodel/sec_dm_main_tables/ssec_dm_gaia_source.html
        job = Gaia.launch_job(
            "select SOURCE_ID, REF_EPOCH, RA, DEC, PARALLAX, PMRA, PMDEC, phot_g_mean_mag from gaiadr2.gaia_source "
            "where SOURCE_ID IN (" + ",".join(targets_table["GAIA"].data) + ") "
        )
        gaia_table = job.get_results()

        if require_all and len(gaia_table) != len(targets_table):
            return None

        # some of the results are missing proper motion & parallax - fill the missing values with defaults
        gaia_table["PMRA"] = gaia_table["PMRA"].filled(0)
        gaia_table["PMDEC"] = gaia_table["PMDEC"].filled(0)
        gaia_table["PARALLAX"] = gaia_table["PARALLAX"].filled(1)

        # make a string version of the int64 source id so we can join this table against the tic table
        gaia_table["gaia source id"] = [str(id) for id in gaia_table["SOURCE_ID"]]

        #merge the gaia data into the table we've been building
        targets_table = join(targets_table, gaia_table, keys_left="GAIA", keys_right="gaia source id")

        #define a distance column based on gaia parallax
        targets_table["Distance"] = 1 / np.abs(targets_table["PARALLAX"]) * u.parsec * u.mas

        # make a SkyCoord object for the RA/DEC of all the objects.
        # the SkyCoord object handles proper motion nicely, so PMRA and PMDEC are in there too
        gaia_coords = SkyCoord(
            targets_table["RA"],
            targets_table["DEC"],
            targets_table["Distance"],
            pm_ra_cosdec=targets_table["PMRA"],
            pm_dec=targets_table["PMDEC"],
            frame="icrs",
            obstime=Time(targets_table["REF_EPOCH"], format="jyear", scale="tdb"),
        )

        # apply proper motion back to J2000
        j2000_coords = gaia_coords.apply_space_motion(Time(2000.0, format="jyear", scale="tdb"))

        targets_table["RA"] = j2000_coords.ra
        targets_table["Dec"] = j2000_coords.dec

        return targets_table
