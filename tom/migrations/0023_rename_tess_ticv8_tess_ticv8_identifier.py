# Generated by Django 4.2.7 on 2024-01-29 18:13

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("tom", "0022_alter_tess_ticv8_tess_ticv8"),
    ]

    operations = [
        migrations.RenameField(
            model_name="tess_ticv8",
            old_name="Tess_TICv8",
            new_name="Identifier",
        ),
    ]
