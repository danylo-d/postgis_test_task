from rest_framework import serializers
from django.contrib.gis.geos import Point

from geo.models import Place


class PointFieldSerializer(serializers.Field):
    def to_representation(self, value):
        if isinstance(value, Point):
            return {"type": "Point", "coordinates": [value.x, value.y]}
        return super().to_representation(value)


class PlaceSerializer(serializers.ModelSerializer):
    longitude = serializers.FloatField(write_only=True)
    latitude = serializers.FloatField(write_only=True)
    geom = PointFieldSerializer(read_only=True)

    class Meta:
        model = Place
        fields = ["id", "name", "description", "longitude", "latitude", "geom"]

    def create(self, validated_data):
        longitude = validated_data.pop("longitude", None)
        latitude = validated_data.pop("latitude", None)
        if longitude is not None and latitude is not None:
            geom = Point(longitude, latitude, srid=4326)
            validated_data["geom"] = geom
        return super().create(validated_data)

    def update(self, instance, validated_data):
        longitude = validated_data.pop("longitude", None)
        latitude = validated_data.pop("latitude", None)
        if longitude is not None and latitude is not None:
            instance.geom = Point(longitude, latitude, srid=4326)
        return super().update(instance, validated_data)


class PlaceListSerializer(PlaceSerializer):
    geom = serializers.SerializerMethodField()

    class Meta:
        model = Place
        fields = ["id", "name", "longitude", "latitude", "geom"]

    @staticmethod
    def get_geom(obj):
        if isinstance(obj.geom, Point):
            return {"longitude": obj.geom.x, "latitude": obj.geom.y}
        return None
