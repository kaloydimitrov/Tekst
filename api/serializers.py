from rest_framework import serializers
from spaces.models import Space, Tag


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ['name']


class SpaceSerializer(serializers.ModelSerializer):
    tags = TagSerializer(many=True)

    class Meta:
        model = Space
        fields = ['name', 'description', 'tags']
