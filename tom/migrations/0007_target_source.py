# Generated by Django 4.2.7 on 2023-11-16 23:48

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("tom", "0006_remove_otherrawdata_size_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="target",
            name="source",
            field=models.CharField(default="", max_length=200),
            preserve_default=False,
        ),
    ]
