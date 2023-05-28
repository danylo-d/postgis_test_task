from django.db import models

from django.contrib.gis.db import models


class Place(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    geom = models.PointField()
