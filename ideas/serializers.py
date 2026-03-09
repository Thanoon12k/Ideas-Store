"""
DRF Serializers for the Ideas Store API.
"""
from rest_framework import serializers
from .models import Idea, IdeaImage


class IdeaImageSerializer(serializers.ModelSerializer):
    """Serializer for idea images."""

    class Meta:
        model = IdeaImage
        fields = ['id', 'image', 'caption', 'uploaded_at']
        read_only_fields = ['id', 'uploaded_at']


class IdeaSerializer(serializers.ModelSerializer):
    """Serializer for ideas with nested images."""
    images = IdeaImageSerializer(many=True, read_only=True)

    class Meta:
        model = Idea
        fields = ['id', 'title', 'description', 'voice_note', 'created_at', 'updated_at', 'images']
        read_only_fields = ['id', 'created_at', 'updated_at']


class IdeaCreateSerializer(serializers.ModelSerializer):
    """Serializer for creating ideas via API."""

    class Meta:
        model = Idea
        fields = ['id', 'title', 'description', 'voice_note']
        read_only_fields = ['id']
