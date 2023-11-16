# Generated by Django 4.2.7 on 2023-11-16 21:58

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("tom", "0004_observation_purpose_alter_target_dec_alter_target_ra"),
    ]

    operations = [
        migrations.CreateModel(
            name="ObservationPurpose",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("purpose", models.CharField(max_length=30)),
            ],
        ),
        migrations.AlterField(
            model_name="observation",
            name="purpose",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to="tom.observationpurpose"
            ),
        ),
    ]
