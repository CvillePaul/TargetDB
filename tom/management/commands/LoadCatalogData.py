from collections import defaultdict
from astropy.table import Table
from astroquery.gaia import Gaia
from astroquery.mast import Catalogs
from django.core.management.base import BaseCommand
from tom import models


class Command(BaseCommand):
    help = "Retrieves catalog data for all catalog objects associated with all Targets"

    def handle(self, *_, **options) -> None:
        # organize by catalog for more efficient querying
        id_dict = defaultdict(set)
        for association in models.CatalogAssociation.objects.all():
            id_dict[association.catalog].add(association.catalog_id)

        # load each type of catalog into its own table
        for catalog, objects in id_dict.items():
            match catalog:
                case "TESS TICv8":
                    self.load_tess_objects(objects)
                case "GAIA DR2":
                    self.load_gaia2_targets(objects)
                case "GAIA DR3":
                    self.load_gaia3_targets(objects)
                case "TESS/Goddard/VSG quadruple candidate (Kostov)" | "White Dwarf Binary":
                    pass  # no online data available for these catalogs
                case _:
                    self.stderr.write(self.style.ERROR(f"Unknown catalog: {catalog}"))
                    return

    def load_tess_objects(self, objects) -> None:
        # retrieve all objects by TIC ID from the TIC catalog
        # TIC fields: https://mast.stsci.edu/api/v0/_t_i_cfields.html
        tic_table = Catalogs.query_criteria(catalog="Tic", ID=objects)
        tic_table.rename_column("ID", "Identifier")

        if len(tic_table) != len(objects):
            self.stderr.write(
                self.style.ERROR(
                    f"Tic query returned {len(tic_table)} instead of {len(objects)} entries"
                )
            )
            return

        num_created, num_updated = 0, 0
        for tic_object in tic_table:
            vals = {
                key: val
                for key, val in zip(tic_object.keys(), tic_object.values())
                if val != "masked"
            }
            identifier = vals.pop("Identifier")
            _, created = models.Tess_TICv8.objects.update_or_create(
                defaults=vals, Identifier=identifier
            )
            if created:
                num_created += 1
            else:
                num_updated += 1
        self.stderr.write(
            self.style.SUCCESS(
                f"Created {num_created} and updated {num_updated} TESS objects"
            )
        )

        # TESS links their TIC objects to GAIA DR2 objects, so make sure those are loaded as well
        self.load_gaia2_targets(tic_table["GAIA"])

    def load_gaia2_targets(self, objects) -> None:
        # hit the MAST database
        # GAIA fields: https://gea.esac.esa.int/archive/documentation/GDR2/Gaia_archive/chap_datamodel/sec_dm_main_tables/ssec_dm_gaia_source.html
        gaia_table = self.load_gaia_targets("gaiadr2.gaia_source", objects)
        num_created, num_updated = 0, 0
        for gaia_object in gaia_table:
            vals = {
                key: val
                for key, val in zip(gaia_object.keys(), gaia_object.values())
                if val != "masked"
            }
            identifier = vals.pop("SOURCE_ID")
            _, created = models.Gaia_DR2.objects.update_or_create(
                defaults=vals, source_id=identifier
            )
            if created:
                num_created += 1
            else:
                num_updated += 1

        self.stderr.write(
            self.style.SUCCESS(
                f"Created {num_created} and updated {num_updated} Gaia DR2 objects"
            )
        )

    def load_gaia3_targets(self, objects) -> None:
        # hit the MAST database
        # GAIA fields: https://gea.esac.esa.int/archive/documentation/GDR3/Gaia_archive/chap_datamodel/sec_dm_main_source_catalogue/ssec_dm_gaia_source.html
        gaia_table = self.load_gaia_targets("gaiadr3.gaia_source", objects)
        num_created, num_updated = 0, 0
        for gaia_object in gaia_table:
            vals = {
                key: val
                for key, val in zip(gaia_object.keys(), gaia_object.values())
                if val != "masked"
            }
            identifier = vals.pop("SOURCE_ID")
            _, created = models.Gaia_DR3.objects.update_or_create(
                defaults=vals, source_id=identifier
            )
            if created:
                num_created += 1
            else:
                num_updated += 1

        self.stderr.write(
            self.style.SUCCESS(
                f"Created {num_created} and updated {num_updated} Gaia DR3 objects"
            )
        )

    def load_gaia_targets(self, table_name: str, objects) -> Table:
        # retrieve all objects by their associated GAIA IDs
        job = Gaia.launch_job(
            f"select * from {table_name} where SOURCE_ID IN ({", ".join(objects)})"
        )
        gaia_table = job.get_results()

        if len(gaia_table) != len(objects):
            self.stderr.write(
                self.style.ERROR(
                    f"Tic query returned {len(gaia_table)} instead of {len(objects)} entries"
                )
            )
            return

        # some of the results are missing proper motion & parallax - fill the missing values with defaults
        gaia_table["pmra"] = gaia_table["pmra"].filled(0)
        gaia_table["pmdec"] = gaia_table["pmdec"].filled(0)
        gaia_table["parallax"] = gaia_table["parallax"].filled(1e-3)

        return gaia_table
