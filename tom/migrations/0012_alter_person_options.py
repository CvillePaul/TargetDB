# Generated by Django 4.2.7 on 2023-11-17 18:05

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("tom", "0011_remove_scienceresult_author_scienceresult_author"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="person",
            options={
                "ordering": ["last_name", "first_name"],
                "verbose_name_plural": "People",
            },
        ),
    ]