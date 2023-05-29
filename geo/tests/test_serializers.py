from django.test import TestCase
from django.contrib.gis.geos import Point

from geo.models import Place
from geo.serializers import PointFieldSerializer, PlaceListSerializer


class PointFieldSerializerTestCase(TestCase):
    def test_to_representation(self):
        serializer = PointFieldSerializer()
        point = Point(1.23, 4.56, srid=4326)
        representation = serializer.to_representation(point)
        expected_representation = {"type": "Point", "coordinates": [1.23, 4.56]}
        self.assertEqual(representation, expected_representation)

    def test_to_internal_value(self):
        serializer = PointFieldSerializer()
        data = "1.23,4.56"
        internal_value = serializer.to_internal_value(data)
        expected_internal_value = Point(1.23, 4.56, srid=4326)
        self.assertEqual(internal_value, expected_internal_value)

    def test_get_geom(self):
        serializer = PlaceListSerializer()
        place_instance = Place.objects.create(
            name="Test Place", geom=Point(1.23, 4.56, srid=4326)
        )
        geom = serializer.get_geom(place_instance)
        expected_geom = [1.23, 4.56]
        self.assertEqual(geom, expected_geom)
