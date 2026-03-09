"""
API URL routing for the Ideas Store.
"""
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .api_views import IdeaViewSet, IdeaImageViewSet

router = DefaultRouter()
router.register(r'ideas', IdeaViewSet, basename='api-idea')
router.register(r'images', IdeaImageViewSet, basename='api-image')

urlpatterns = [
    path('', include(router.urls)),
]
