# Generated by Django 4.2.1 on 2023-05-29 12:34

import django.contrib.gis.db.models.fields
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Place",
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
                ("name", models.CharField(max_length=255)),
                ("description", models.TextField(blank=True, null=True)),
                ("geom", django.contrib.gis.db.models.fields.PointField(srid=4326)),
            ],
            options={
                "indexes": [
                    models.Index(fields=["geom"], name="geo_place_geom_186ef4_idx")
                ],
            },
        ),
    ]
