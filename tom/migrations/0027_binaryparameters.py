# Generated by Django 4.2.7 on 2024-01-30 18:23

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("tom", "0026_alter_gaia_dr3_designation_alter_gaia_dr3_source_id"),
    ]

    operations = [
        migrations.CreateModel(
            name="BinaryParameters",
            fields=[
                (
                    "scienceresult_ptr",
                    models.OneToOneField(
                        auto_created=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        parent_link=True,
                        primary_key=True,
                        serialize=False,
                        to="tom.scienceresult",
                    ),
                ),
                (
                    "member",
                    models.CharField(
                        help_text="Name of component, eg A or B", max_length=50
                    ),
                ),
                ("period", models.FloatField(help_text="Period in days")),
                ("t0_primary", models.FloatField(help_text="Date in BJD")),
                ("t0_secondary", models.FloatField(help_text="Date in BJD", null=True)),
                ("duration_primary", models.FloatField(help_text="Duration in hours")),
                (
                    "duration_secondary",
                    models.FloatField(help_text="Duration in hours", null=True),
                ),
                ("depth_primary", models.FloatField(null=True)),
                ("depth_secondary", models.FloatField(null=True)),
            ],
            bases=("tom.scienceresult",),
        ),
    ]
