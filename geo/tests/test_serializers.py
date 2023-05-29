from django.test import TestCase
from django.contrib.gis.geos import Point
from geo.models import Place
from geo.serializers import PlaceSerializer, PlaceListSerializer


class PlaceSerializerTest(TestCase):
    def test_create(self):
        serializer = PlaceSerializer()
        validated_data = {
            'name': 'Test Place',
            'description': 'Test Description',
            'longitude': 1.23,
            'latitude': 4.56
        }
        place = serializer.create(validated_data)
        self.assertIsInstance(place, Place)
        self.assertEqual(place.name, 'Test Place')
        self.assertEqual(place.description, 'Test Description')
        self.assertEqual(place.geom, Point(1.23, 4.56, srid=4326))

    def test_update(self):
        place = Place.objects.create(name='Test Place', description='Old Description', geom=Point(0, 0, srid=4326))
        serializer = PlaceSerializer(instance=place)
        validated_data = {
            'name': 'Updated Place',
            'description': 'New Description',
            'longitude': 7.89,
            'latitude': 0.12
        }
        updated_place = serializer.update(place, validated_data)
        self.assertEqual(updated_place.name, 'Updated Place')
        self.assertEqual(updated_place.description, 'New Description')
        self.assertEqual(updated_place.geom, Point(7.89, 0.12, srid=4326))


class PlaceListSerializerTest(TestCase):
    def test_get_geom(self):
        place = Place(name="Test Place", geom=Point(1.23, 4.56, srid=4326))
        serializer = PlaceListSerializer(instance=place)
        geom = serializer.get_geom(place)
        self.assertEqual(geom, {"longitude": 1.23, "latitude": 4.56})
