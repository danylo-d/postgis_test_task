from django.urls import path, include
from rest_framework import routers

from geo.views import PlaceViewSet

router = routers.DefaultRouter()
router.register("places", PlaceViewSet)
urlpatterns = [
    path("", include(router.urls)),
    path(
        "nearest_place/",
        PlaceViewSet.as_view({"get": "nearest_place"}),
        name="place-nearest",
    ),
]

app_name = "geo"
