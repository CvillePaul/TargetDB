# Generated by Django 4.2.7 on 2023-12-20 17:54

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("tom", "0009_specklerawdata_datetime_utc"),
    ]

    operations = [
        migrations.RenameField(
            model_name="observingsession",
            old_name="observing_program",
            new_name="observingprogram",
        ),
        migrations.RenameField(
            model_name="specklerawdata",
            old_name="observing_session",
            new_name="observingsession",
        ),
        migrations.RenameField(
            model_name="spectrumrawdata",
            old_name="observing_session",
            new_name="observingsession",
        ),
    ]
