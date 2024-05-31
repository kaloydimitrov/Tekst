from rest_framework import serializers
from spaces.models import Space, Tag


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ['id', 'name']


class SpaceSerializer(serializers.ModelSerializer):
    tags = TagSerializer(many=True, read_only=True, source='tag_set')

    class Meta:
        model = Space
        fields = ['id', 'name', 'description', 'image', 'user', 'created_at', 'updated_at', 'tags']
