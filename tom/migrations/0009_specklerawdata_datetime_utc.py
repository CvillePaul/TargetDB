# Generated by Django 4.2.7 on 2023-12-19 17:20

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("tom", "0008_specklerawdata_channels"),
    ]

    operations = [
        migrations.AddField(
            model_name="specklerawdata",
            name="datetime_utc",
            field=models.DateTimeField(default=datetime.datetime(1970, 1, 1, 0, 0)),
        ),
    ]