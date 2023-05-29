from django.contrib.gis.db import models


class Place(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    geom = models.PointField()

    class Meta:
        indexes = [
            models.Index(fields=["geom"]),
        ]

    def __str__(self):
        return f"{self.name} ({self.geom.x}, {self.geom.y})"
