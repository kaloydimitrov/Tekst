from rest_framework import generics
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.permissions import IsAuthenticated
from spaces.models import Space
from .serializers import SpaceSerializer


# --------------------------------------
# SPACES
# --------------------------------------
class SpaceListView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Space.objects.all()
    serializer_class = SpaceSerializer
    filter_backends = (SearchFilter, OrderingFilter)
    search_fields = ('name', 'description', 'user__username')


class SpaceDetailView(generics.RetrieveAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Space.objects.all()
    serializer_class = SpaceSerializer
