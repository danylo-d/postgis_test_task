from django.test import TestCase
from django.contrib.gis.geos import Point

from geo.models import Place


class PlaceModelTest(TestCase):
    def setUp(self):
        self.place = Place.objects.create(
            name="Test Place", description="Test description", geom=Point(10.0, 20.0, srid=4326)
        )

    def test_place_str_method(self):
        self.assertEqual(str(self.place), "Test Place (10.0, 20.0)")
