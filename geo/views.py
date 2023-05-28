from django.contrib.gis.db.models.functions import Distance
from django.contrib.gis.geos import Point
from rest_framework import viewsets, status
from rest_framework.decorators import action, api_view
from rest_framework.response import Response

from geo.models import Place
from geo.serializers import PlaceSerializer, PlaceListSerializer


class PlaceViewSet(viewsets.ModelViewSet):
    queryset = Place.objects.all()
    serializer_class = PlaceSerializer

    def get_serializer_class(self):
        if self.action == "list":
            return PlaceListSerializer
        return super().get_serializer_class()

    def get_nearest_place(self, request):
        latitude = request.query_params.get("latitude")
        longitude = request.query_params.get("longitude")

        if latitude is not None and longitude is not None:
            point = Point(float(longitude), float(latitude), srid=4326)
            nearest_place = (
                self.queryset.annotate(distance=Distance("geom", point))
                .order_by("distance")
                .first()
            )
            serializer = self.get_serializer(nearest_place)
            return Response(serializer.data)

        return Response(
            {"error": "Latitude and longitude parameters are required."},
            status=status.HTTP_400_BAD_REQUEST,
        )

    @action(detail=True, methods=["get"])
    def nearest_place(self, request, *args, **kwargs):
        instance = self.get_object()

        current_location = instance.geom

        nearest_place = (
            self.queryset.annotate(distance=Distance("geom", current_location))
            .exclude(id=instance.id)
            .order_by("distance")
            .first()
        )

        serializer = self.get_serializer(instance)
        serializer_data = serializer.data
        serializer_data["nearest_place"] = PlaceSerializer(
            nearest_place, context=self.get_serializer_context()
        ).data

        return Response(serializer_data["nearest_place"])
