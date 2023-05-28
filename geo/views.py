from rest_framework import viewsets

from geo.models import Place
from geo.serializers import PlaceSerializer


# Create your views here.
class PlaceViewSet(viewsets.ModelViewSet):
    queryset = Place.objects.all()
    serializer_class = PlaceSerializer
