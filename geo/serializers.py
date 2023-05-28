from rest_framework import serializers
from django.contrib.gis.geos import Point

from geo.models import Place


class PointFieldSerializer(serializers.Field):
    def to_representation(self, value):
        if isinstance(value, Point):
            return {"type": "Point", "coordinates": [value.x, value.y]}
        return super().to_representation(value)

    def to_internal_value(self, data):
        if isinstance(data, str):
            try:
                x, y = map(float, data.split(","))
                return Point(x, y, srid=4326)
            except ValueError:
                raise serializers.ValidationError(
                    "Invalid geom value. Must be in the format of 'x, y'."
                )


class PlaceSerializer(serializers.ModelSerializer):
    geom = PointFieldSerializer()

    class Meta:
        model = Place
        fields = ["id", "name", "description", "geom"]


class PlaceListSerializer(PlaceSerializer):
    geom = serializers.SerializerMethodField()

    class Meta:
        model = Place
        fields = ["id", "name", "geom"]

    @staticmethod
    def get_geom(obj):
        if isinstance(obj.geom, Point):
            return [obj.geom.x, obj.geom.y]
        return None
