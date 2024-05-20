from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from spaces.models import Space, Tag
from .serializers import SpaceSerializer
from rest_framework.permissions import IsAuthenticated


class SpaceAPIView(APIView):
    permission_classes = [IsAuthenticated]

    @staticmethod
    def post(request, *args, **kwargs):
        serializer = SpaceSerializer(data=request.data)
        if serializer.is_valid():
            if len(request.data.get('tags', [])) < 10:
                return Response({'error': 'A space must have at least 10 tags.'}, status=status.HTTP_400_BAD_REQUEST)

            space = Space.objects.create(
                name=serializer.validated_data['name'],
                description=serializer.validated_data['description'],
                user=request.user
            )

            tags_data = serializer.validated_data['tags']
            for tag_data in tags_data:
                Tag.objects.create(name=tag_data['name'], space=space)

            return Response({'message': 'Space created successfully with tags.'}, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
