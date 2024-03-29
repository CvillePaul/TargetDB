# Generated by Django 4.2.7 on 2023-12-01 18:27

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    initial = True

    dependencies = []

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
                ("purpose", models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name="Observatory",
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
                ("nickname", models.CharField(max_length=15)),
                ("name", models.CharField(max_length=100)),
                ("iau_code", models.CharField(max_length=10)),
            ],
        ),
        migrations.CreateModel(
            name="ObservingProgram",
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
                ("name", models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name="ObservingSession",
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
                ("utc_date", models.DateField()),
                ("equipment", models.CharField(max_length=100)),
                (
                    "observatory",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="tom.observatory",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Person",
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
                ("first_name", models.CharField(max_length=50)),
                ("last_name", models.CharField(max_length=50)),
                ("email", models.CharField(max_length=100)),
                ("affiliation", models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name="Target",
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
                ("local_id", models.CharField(max_length=100, unique=True)),
                (
                    "source",
                    models.CharField(
                        blank=True,
                        help_text="How target was identified/discovered",
                        max_length=100,
                    ),
                ),
                ("ra", models.FloatField(verbose_name="RA (deg)")),
                ("dec", models.FloatField(verbose_name="Dec (deg)")),
                ("pmra", models.FloatField(default=0, verbose_name="PM RA (mas/yr)")),
                ("pmdec", models.FloatField(default=0, verbose_name="PM Dec (mas/yr)")),
                (
                    "distance",
                    models.FloatField(default=0, verbose_name="Distance (pc)"),
                ),
                ("magnitude", models.FloatField()),
            ],
        ),
        migrations.CreateModel(
            name="TargetIdType",
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
                ("id_type", models.CharField(max_length=100, unique=True)),
                ("comment", models.CharField(blank=True, max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name="TargetList",
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
                ("name", models.CharField(max_length=200)),
                ("created", models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name="CalibrationTarget",
            fields=[
                (
                    "target_ptr",
                    models.OneToOneField(
                        auto_created=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        parent_link=True,
                        primary_key=True,
                        serialize=False,
                        to="tom.target",
                    ),
                ),
            ],
            bases=("tom.target",),
        ),
        migrations.CreateModel(
            name="TargetListMember",
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
                ("target", models.ManyToManyField(to="tom.target")),
                (
                    "target_list",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="tom.targetlist"
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="TargetIdentifier",
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
                ("identifier", models.CharField(max_length=100)),
                (
                    "id_type",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="tom.targetidtype",
                    ),
                ),
                (
                    "target",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="tom.target"
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="SpectrumRawData",
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
                ("uri", models.CharField(max_length=200)),
                ("jd_btd", models.CharField(default="", max_length=30)),
                ("fiber", models.CharField(default="", max_length=20)),
                ("cross_disperser", models.CharField(default="", max_length=100)),
                ("arm", models.CharField(default="", max_length=30)),
                ("exposure_time", models.FloatField(default=0)),
                (
                    "observing_session",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="tom.observingsession",
                    ),
                ),
                (
                    "target",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="tom.target"
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
        ),
        migrations.CreateModel(
            name="SpeckleRawData",
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
                ("uri", models.CharField(max_length=200)),
                ("gain", models.PositiveIntegerField(default=0)),
                ("exposure_time_ms", models.PositiveIntegerField(default=0)),
                ("num_sequences", models.PositiveIntegerField(default=0)),
                (
                    "observing_session",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="tom.observingsession",
                    ),
                ),
                (
                    "target",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="tom.target"
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
        ),
        migrations.CreateModel(
            name="ScienceResult",
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
                ("type", models.CharField(max_length=30)),
                ("author", models.CharField(default="", max_length=200)),
                ("uri", models.CharField(max_length=200)),
                (
                    "target",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="tom.target"
                    ),
                ),
            ],
        ),
        migrations.AddField(
            model_name="observingsession",
            name="observers",
            field=models.ManyToManyField(to="tom.person"),
        ),
        migrations.AddField(
            model_name="observingsession",
            name="observing_program",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to="tom.observingprogram"
            ),
        ),
        migrations.AddField(
            model_name="observingsession",
            name="purpose",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to="tom.observationpurpose"
            ),
        ),
        migrations.CreateModel(
            name="ScienceTarget",
            fields=[
                (
                    "target_ptr",
                    models.OneToOneField(
                        auto_created=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        parent_link=True,
                        primary_key=True,
                        serialize=False,
                        to="tom.target",
                    ),
                ),
                ("calibrations", models.ManyToManyField(to="tom.calibrationtarget")),
            ],
            bases=("tom.target",),
        ),
    ]
