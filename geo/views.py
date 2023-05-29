from django.contrib.gis.db.models.functions import Distance
from django.contrib.gis.geos import Point
from django.contrib.gis.measure import D
from drf_spectacular.utils import extend_schema, OpenApiParameter
from rest_framework import viewsets, status
from rest_framework.decorators import action
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

    @extend_schema(
        parameters=[
            OpenApiParameter(
                name="longitude",
                type=float,
                description="Longitude of the desired location.",
                required=False,
            ),
            OpenApiParameter(
                name="latitude",
                type=float,
                description="Latitude of the desired location.",
                required=False,
            ),
        ]
    )
    def get_nearest_place(self, request):
        """
        Get the nearest existing location in the DB
        to the desired location according to the provided latitude and longitude.

        Parameters:
        - longitude (float): Longitude of the desired location.
        - latitude (float): Latitude of the desired location.

        Returns:
        - 200 OK: Nearest place found, serialized data of the nearest place.
        - 400 Bad Request: Longitude and latitude parameters are required.
        - 400 Bad Request: Invalid longitude or latitude values provided.
        """
        longitude = request.query_params.get("longitude")
        latitude = request.query_params.get("latitude")

        if latitude is not None and longitude is not None:
            try:
                point = Point(float(longitude), float(latitude), srid=4326)
                nearest_place = (
                    self.queryset.filter(geom__distance_lte=(point, D(m=10000)))
                    .annotate(distance=Distance("geom", point))
                    .order_by("distance")
                    .first()
                )
                serializer = self.get_serializer(nearest_place)
                return Response(serializer.data)
            except ValueError:
                return Response(
                    {"error": "Invalid longitude or latitude values provided."},
                    status=status.HTTP_400_BAD_REQUEST,
                )
        else:
            return Response(
                {"error": "Longitude and latitude parameters are required."},
                status=status.HTTP_400_BAD_REQUEST,
            )

    @action(detail=True, methods=["get"])
    def nearest_place(self, request, *args, **kwargs):
        """
        Get the nearest place to the current location of the specified place.

        Parameters:
        - None

        Returns:
        - 200 OK: Nearest place found, serialized data of the nearest place.
        """
        instance = self.get_object()

        current_location = instance.geom

        nearest_place = (
            self.queryset.filter(geom__distance_lte=(current_location, D(m=10000)))
            .annotate(distance=Distance("geom", current_location))
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

    def list(self, request, *args, **kwargs):
        """
        Get all places in the DB.

        Parameters:
        - None

        Returns:
        - 200 OK: All places found, serialized data of the places.
        """
        return super().list(request, *args, **kwargs)

    def retrieve(self, request, *args, **kwargs):
        """
        Get a specific place in the DB.

        Parameters:
        - None

        Returns:
        - 200 OK: Specific place found, serialized data of the place.
        """
        return super().retrieve(request, *args, **kwargs)

    def create(self, request, *args, **kwargs):
        """
        Create a new place in the DB.

        Parameters:
        - None

        Returns:
        - 201 Created: New place created, serialized data of the place.
        """
        return super().create(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        """
        Update a specific place in the DB.

        Parameters:
        - None

        Returns:
        - 200 OK: Specific place updated, serialized data of the place.
        """
        return super().update(request, *args, **kwargs)

    def partial_update(self, request, *args, **kwargs):
        """
        Update a specific place in the DB.

        Parameters:
        - None

        Returns:
        - 200 OK: Specific place updated, serialized data of the place.
        """
        return super().partial_update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        """
        Delete a specific place in the DB.

        Parameters:
        - None

        Returns:
        - 200 OK: Specific place deleted.
        """
        return super().destroy(request, *args, **kwargs)
