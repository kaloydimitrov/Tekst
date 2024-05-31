from rest_framework import generics
from spaces.models import Space
from .serializers import SpaceSerializer


class SpaceDetail(generics.RetrieveAPIView):
    queryset = Space.objects.all()
    serializer_class = SpaceSerializer
