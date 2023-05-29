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

    def test_get_geom(self):
        serializer = PlaceListSerializer()
        place_instance = Place.objects.create(
            name="Test Place", geom=Point(1.23, 4.56, srid=4326)
        )
        geom = serializer.get_geom(place_instance)
        expected_geom = {"longitude": 1.23, "latitude": 4.56}
        self.assertEqual(geom, expected_geom)
