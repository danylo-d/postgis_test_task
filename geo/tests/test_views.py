from django.test import RequestFactory, TestCase
from django.contrib.gis.geos import Point
from rest_framework import status

from geo.models import Place
from geo.views import PlaceViewSet


class PlaceViewSetTest(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.view = PlaceViewSet.as_view({"get": "get_nearest_place"})
        self.place = Place.objects.create(
            name="Place 1", description="Description 1", geom=Point(0, 0, srid=4326)
        )

    def test_get_nearest_place_success(self):
        request = self.factory.get(
            "/places/nearest-place", {"latitude": 1, "longitude": 1}
        )
        response = self.view(request)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["name"], self.place.name)

    def test_get_nearest_place_wrong_parameters(self):
        request = self.factory.get("/places/nearest-place/?latitude=12.34&longitude=test+")
        response = self.view(request)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            response.data["error"], "Invalid longitude or latitude values provided."
        )

    def test_get_nearest_place_missing_parameters(self):
        request = self.factory.get("/places/nearest-place")
        response = self.view(request)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            response.data["error"], "Longitude and latitude parameters are required."
        )

    def test_nearest_place_excludes_current_place(self):
        other_place = Place.objects.create(
            name="Place 2", description="Description 2", geom=Point(2, 2, srid=4326)
        )
        request = self.factory.get("/places/{}/nearest_place".format(self.place.id))
        response = PlaceViewSet.as_view({"get": "nearest_place"})(
            request, pk=self.place.id
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["name"], other_place.name)

    def test_nearest_place_handles_invalid_place_id(self):
        invalid_id = 9999
        request = self.factory.get("/places/{}/nearest_place".format(invalid_id))
        response = PlaceViewSet.as_view({"get": "nearest_place"})(
            request, pk=invalid_id
        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
