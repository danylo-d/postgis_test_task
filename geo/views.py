from django.contrib.gis.db.models.functions import Distance
from django.contrib.gis.geos import Point
from drf_spectacular.utils import extend_schema, OpenApiParameter
from rest_framework import viewsets, status
from rest_framework.response import Response

from geo.models import Place
from geo.serializers import PlaceSerializer, PlaceListSerializer


class PlaceViewSet(viewsets.ModelViewSet):
    queryset = Place.objects.all()
    serializer_class = PlaceSerializer

    def get_serializer_class(self):
        return (
            PlaceListSerializer
            if self.action == "list"
            else super().get_serializer_class()
        )

    MAX_DISTANCE = 10  # value in degrees

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
    def nearest_place(self, request, *args, **kwargs):
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
        longitude = request.query_params.get("longitude", None)
        latitude = request.query_params.get("latitude", None)

        if longitude and latitude:
            try:
                point = Point(float(longitude), float(latitude), srid=4326)
                max_distance = self.MAX_DISTANCE

                nearest_place = (
                    self.queryset.filter(geom__dwithin=(point, max_distance))
                    .annotate(distance=Distance("geom", point))
                    .order_by("distance")
                    .first()
                )

                if nearest_place is not None:
                    serializer = self.get_serializer(nearest_place)
                    return Response(serializer.data)
                else:
                    return Response(
                        {"message": "No nearest place found."},
                        status=status.HTTP_404_NOT_FOUND,
                    )
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
