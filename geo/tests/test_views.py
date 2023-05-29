from django.test import RequestFactory, TestCase
from django.contrib.gis.geos import Point
from rest_framework import status

from geo.models import Place
from geo.views import PlaceViewSet


class PlaceViewSetTest(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.view = PlaceViewSet.as_view({"get": "nearest_place"})
        self.place = Place.objects.create(
            name="Place 1", description="Description 1", geom=Point(0, 0, srid=4326)
        )

    def test_nearest_place_success(self):
        request = self.factory.get("/nearest-place", {"latitude": 1, "longitude": 1})
        response = self.view(request)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["name"], self.place.name)

    def test_nearest_place_wrong_parameters(self):
        request = self.factory.get("/nearest-place/?latitude=12.34&longitude=test+")
        response = self.view(request)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            response.data["error"], "Invalid longitude or latitude values provided."
        )

    def test_nearest_place_missing_parameters(self):
        request = self.factory.get("/nearest-place")
        response = self.view(request)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            response.data["error"], "Longitude and latitude parameters are required."
        )
