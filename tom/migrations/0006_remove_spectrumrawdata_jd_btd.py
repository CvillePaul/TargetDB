# Generated by Django 4.2.7 on 2023-12-17 17:04

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("tom", "0005_spectrumrawdata_datetime_utc"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="spectrumrawdata",
            name="jd_btd",
        ),
    ]
