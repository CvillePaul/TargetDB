# Generated by Django 4.2.7 on 2024-01-29 20:01

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("tom", "0024_alter_tess_ticv8_identifier"),
    ]

    operations = [
        migrations.AlterField(
            model_name="gaia_dr2",
            name="DESIGNATION",
            field=models.CharField(max_length=100, null=True, unique=True),
        ),
        migrations.AlterField(
            model_name="gaia_dr2",
            name="source_id",
            field=models.CharField(max_length=100, null=True, unique=True),
        ),
    ]
