# Generated by Django 4.2.7 on 2024-01-08 15:41

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("tom", "0011_rename_channels_specklerawdata_channel_and_more"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="sciencetarget",
            name="calibrations",
        ),
        migrations.DeleteModel(
            name="CalibrationTarget",
        ),
    ]
