# Generated by Django 4.2.7 on 2023-12-17 17:03

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("tom", "0004_targetlist_description"),
    ]

    operations = [
        migrations.AddField(
            model_name="spectrumrawdata",
            name="datetime_utc",
            field=models.DateTimeField(default=datetime.datetime(1970, 1, 1, 0, 0)),
        ),
    ]