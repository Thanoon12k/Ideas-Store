"""
DRF API Views for the Ideas Store.
"""
from rest_framework import viewsets, status, parsers
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Idea, IdeaImage
from .serializers import IdeaSerializer, IdeaCreateSerializer, IdeaImageSerializer


class IdeaViewSet(viewsets.ModelViewSet):
    """
    API endpoint for ideas.
    Supports: list, create, retrieve, update, partial_update, destroy.
    """
    permission_classes = [IsAuthenticated]
    parser_classes = [parsers.MultiPartParser, parsers.FormParser, parsers.JSONParser]

    def get_queryset(self):
        return Idea.objects.prefetch_related('images').filter(user=self.request.user)

    def get_serializer_class(self):
        if self.action in ['create', 'update', 'partial_update']:
            return IdeaCreateSerializer
        return IdeaSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    @action(detail=True, methods=['post'], url_path='upload-image')
    def upload_image(self, request, pk=None):
        """Upload an image to an existing idea."""
        idea = self.get_object()
        image_file = request.FILES.get('image')
        caption = request.data.get('caption', '')

        if not image_file:
            return Response(
                {'error': 'No image file provided.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        if image_file.size > 5 * 1024 * 1024:
            return Response(
                {'error': 'Image must be less than 5 MB.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        idea_image = IdeaImage.objects.create(
            idea=idea,
            image=image_file,
            caption=caption
        )
        serializer = IdeaImageSerializer(idea_image)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class IdeaImageViewSet(viewsets.ModelViewSet):
    """
    API endpoint for idea images.
    Supports: list, create, retrieve, destroy.
    """
    def get_queryset(self):
        return IdeaImage.objects.filter(idea__user=self.request.user)

    serializer_class = IdeaImageSerializer
    permission_classes = [IsAuthenticated]
    parser_classes = [parsers.MultiPartParser, parsers.FormParser]
    http_method_names = ['get', 'post', 'delete', 'head', 'options']
