# Generated by Django 4.2.7 on 2024-01-29 20:02

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("tom", "0025_alter_gaia_dr2_designation_alter_gaia_dr2_source_id"),
    ]

    operations = [
        migrations.AlterField(
            model_name="gaia_dr3",
            name="DESIGNATION",
            field=models.CharField(max_length=100, null=True, unique=True),
        ),
        migrations.AlterField(
            model_name="gaia_dr3",
            name="source_id",
            field=models.CharField(max_length=100, null=True, unique=True),
        ),
    ]