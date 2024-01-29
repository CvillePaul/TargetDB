# Generated by Django 4.2.7 on 2024-01-29 16:52

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("tom", "0017_delete_sciencetarget"),
    ]

    operations = [
        migrations.CreateModel(
            name="Gaia_DR2",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("solution_id", models.BigIntegerField()),
                ("DESIGNATION", models.CharField(default="", max_length=100)),
                ("source_id", models.BigIntegerField()),
                ("random_index", models.BigIntegerField()),
                ("ref_epoch", models.FloatField()),
                ("ra", models.FloatField()),
                ("ra_error", models.FloatField()),
                ("dec", models.FloatField()),
                ("dec_error", models.FloatField()),
                ("parallax", models.CharField(default="", max_length=100)),
                ("parallax_error", models.CharField(default="", max_length=100)),
                ("parallax_over_error", models.CharField(default="", max_length=100)),
                ("pmra", models.CharField(default="", max_length=100)),
                ("pmra_error", models.CharField(default="", max_length=100)),
                ("pmdec", models.CharField(default="", max_length=100)),
                ("pmdec_error", models.CharField(default="", max_length=100)),
                ("ra_dec_corr", models.FloatField()),
                ("ra_parallax_corr", models.CharField(default="", max_length=100)),
                ("ra_pmra_corr", models.CharField(default="", max_length=100)),
                ("ra_pmdec_corr", models.CharField(default="", max_length=100)),
                ("dec_parallax_corr", models.CharField(default="", max_length=100)),
                ("dec_pmra_corr", models.CharField(default="", max_length=100)),
                ("dec_pmdec_corr", models.CharField(default="", max_length=100)),
                ("parallax_pmra_corr", models.CharField(default="", max_length=100)),
                ("parallax_pmdec_corr", models.CharField(default="", max_length=100)),
                ("pmra_pmdec_corr", models.CharField(default="", max_length=100)),
                ("astrometric_n_obs_al", models.IntegerField()),
                ("astrometric_n_obs_ac", models.IntegerField()),
                ("astrometric_n_good_obs_al", models.IntegerField()),
                ("astrometric_n_bad_obs_al", models.IntegerField()),
                ("astrometric_gof_al", models.FloatField()),
                ("astrometric_chi2_al", models.FloatField()),
                ("astrometric_excess_noise", models.FloatField()),
                ("astrometric_excess_noise_sig", models.FloatField()),
                ("astrometric_params_solved", models.IntegerField()),
                (
                    "astrometric_primary_flag",
                    models.CharField(default="", max_length=100),
                ),
                ("astrometric_weight_al", models.FloatField()),
                (
                    "astrometric_pseudo_colour",
                    models.CharField(default="", max_length=100),
                ),
                (
                    "astrometric_pseudo_colour_error",
                    models.CharField(default="", max_length=100),
                ),
                ("mean_varpi_factor_al", models.FloatField()),
                ("astrometric_matched_observations", models.IntegerField()),
                ("visibility_periods_used", models.IntegerField()),
                ("astrometric_sigma5d_max", models.FloatField()),
                ("frame_rotator_object_type", models.IntegerField()),
                ("matched_observations", models.IntegerField()),
                ("duplicated_source", models.CharField(default="", max_length=100)),
                ("phot_g_n_obs", models.IntegerField()),
                ("phot_g_mean_flux", models.FloatField()),
                ("phot_g_mean_flux_error", models.FloatField()),
                ("phot_g_mean_flux_over_error", models.FloatField()),
                ("phot_g_mean_mag", models.FloatField()),
                ("phot_bp_n_obs", models.IntegerField()),
                ("phot_bp_mean_flux", models.CharField(default="", max_length=100)),
                (
                    "phot_bp_mean_flux_error",
                    models.CharField(default="", max_length=100),
                ),
                (
                    "phot_bp_mean_flux_over_error",
                    models.CharField(default="", max_length=100),
                ),
                ("phot_bp_mean_mag", models.CharField(default="", max_length=100)),
                ("phot_rp_n_obs", models.IntegerField()),
                ("phot_rp_mean_flux", models.CharField(default="", max_length=100)),
                (
                    "phot_rp_mean_flux_error",
                    models.CharField(default="", max_length=100),
                ),
                (
                    "phot_rp_mean_flux_over_error",
                    models.CharField(default="", max_length=100),
                ),
                ("phot_rp_mean_mag", models.CharField(default="", max_length=100)),
                (
                    "phot_bp_rp_excess_factor",
                    models.CharField(default="", max_length=100),
                ),
                ("phot_proc_mode", models.IntegerField()),
                ("bp_rp", models.CharField(default="", max_length=100)),
                ("bp_g", models.CharField(default="", max_length=100)),
                ("g_rp", models.CharField(default="", max_length=100)),
                ("radial_velocity", models.CharField(default="", max_length=100)),
                ("radial_velocity_error", models.CharField(default="", max_length=100)),
                ("rv_nb_transits", models.IntegerField()),
                ("rv_template_teff", models.CharField(default="", max_length=100)),
                ("rv_template_logg", models.CharField(default="", max_length=100)),
                ("rv_template_fe_h", models.CharField(default="", max_length=100)),
                ("phot_variable_flag", models.CharField(default="", max_length=100)),
                ("l", models.FloatField()),
                ("b", models.FloatField()),
                ("ecl_lon", models.FloatField()),
                ("ecl_lat", models.FloatField()),
                ("priam_flags", models.CharField(default="", max_length=100)),
                ("teff_val", models.CharField(default="", max_length=100)),
                ("teff_percentile_lower", models.CharField(default="", max_length=100)),
                ("teff_percentile_upper", models.CharField(default="", max_length=100)),
                ("a_g_val", models.CharField(default="", max_length=100)),
                ("a_g_percentile_lower", models.CharField(default="", max_length=100)),
                ("a_g_percentile_upper", models.CharField(default="", max_length=100)),
                ("e_bp_min_rp_val", models.CharField(default="", max_length=100)),
                (
                    "e_bp_min_rp_percentile_lower",
                    models.CharField(default="", max_length=100),
                ),
                (
                    "e_bp_min_rp_percentile_upper",
                    models.CharField(default="", max_length=100),
                ),
                ("flame_flags", models.CharField(default="", max_length=100)),
                ("radius_val", models.CharField(default="", max_length=100)),
                (
                    "radius_percentile_lower",
                    models.CharField(default="", max_length=100),
                ),
                (
                    "radius_percentile_upper",
                    models.CharField(default="", max_length=100),
                ),
                ("lum_val", models.CharField(default="", max_length=100)),
                ("lum_percentile_lower", models.CharField(default="", max_length=100)),
                ("lum_percentile_upper", models.CharField(default="", max_length=100)),
                ("datalink_url", models.CharField(default="", max_length=100)),
                ("epoch_photometry_url", models.CharField(default="", max_length=100)),
                ("TIC_ID", models.IntegerField()),
                ("TIC_Distance", models.FloatField()),
            ],
        ),
        migrations.RemoveField(
            model_name="gaia_dr3",
            name="target",
        ),
        migrations.RemoveField(
            model_name="tess_ticv8",
            name="target",
        ),
    ]
