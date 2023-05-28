from rest_framework import serializers
from django.contrib.gis.geos import Point

from geo.models import Place


class PointFieldSerializer(serializers.Field):
    def to_representation(self, value):
        if isinstance(value, Point):
            return {"type": "Point", "coordinates": [value.x, value.y]}
        return value

    def to_internal_value(self, data):
        if isinstance(data, str):
            try:
                x, y = map(float, data.split(","))
                return Point(x, y)
            except (ValueError, TypeError):
                pass
        return data


class PlaceSerializer(serializers.ModelSerializer):
    geom = PointFieldSerializer()

    class Meta:
        model = Place
        fields = ("id", "name", "description", "geom")
