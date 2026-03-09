"""
Tests for Ideas Store REST API.
"""
from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from django.core.files.uploadedfile import SimpleUploadedFile
from rest_framework.test import APIClient
from rest_framework import status
from ideas.models import Idea, IdeaImage


class APITestBase(TestCase):
    """Base test class for API tests."""

    def setUp(self):
        """Create test user and authenticated API client."""
        self.client = APIClient()
        self.user = User.objects.create_user(
            username='apiuser',
            password='apipass123!'
        )
        self.client.force_authenticate(user=self.user)

        self.idea = Idea.objects.create(
            user=self.user,
            title='API Test Idea',
            description='Test from API'
        )


class IdeaAPITest(APITestBase):
    """Tests for the Idea API endpoints."""

    def test_list_ideas(self):
        """Test listing all ideas."""
        response = self.client.get('/api/ideas/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 1)

    def test_retrieve_idea(self):
        """Test retrieving a single idea."""
        response = self.client.get(f'/api/ideas/{self.idea.pk}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], 'API Test Idea')

    def test_create_idea(self):
        """Test creating an idea via API."""
        response = self.client.post('/api/ideas/', {
            'title': 'New API Idea',
            'description': 'Created via API',
        })
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(Idea.objects.filter(title='New API Idea').exists())

    def test_update_idea(self):
        """Test updating an idea via API."""
        response = self.client.put(f'/api/ideas/{self.idea.pk}/', {
            'title': 'Updated API Idea',
            'description': 'Updated via API',
        })
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.idea.refresh_from_db()
        self.assertEqual(self.idea.title, 'Updated API Idea')

    def test_partial_update_idea(self):
        """Test PATCH update on an idea."""
        response = self.client.patch(f'/api/ideas/{self.idea.pk}/', {
            'title': 'Patched Title',
        })
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.idea.refresh_from_db()
        self.assertEqual(self.idea.title, 'Patched Title')

    def test_delete_idea(self):
        """Test deleting an idea via API."""
        pk = self.idea.pk
        response = self.client.delete(f'/api/ideas/{pk}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Idea.objects.filter(pk=pk).exists())

    def test_create_idea_no_title(self):
        """Test that title is required."""
        response = self.client.post('/api/ideas/', {
            'description': 'No title idea',
        })
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_unauthenticated_access(self):
        """Test that unauthenticated users cannot access the API."""
        self.client.force_authenticate(user=None)
        response = self.client.get('/api/ideas/')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class IdeaImageAPITest(APITestBase):
    """Tests for the Idea Image API endpoints."""

    def test_upload_image(self):
        """Test uploading an image to an idea via API."""
        image_data = (
            b'\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR'
            b'\x00\x00\x00\x01\x00\x00\x00\x01\x08\x02'
            b'\x00\x00\x00\x90wS\xde\x00\x00\x00\x0c'
            b'IDATx\x9cc\xf8\x0f\x00\x00\x01\x01\x00'
            b'\x05\x18\xd8N\x00\x00\x00\x00IEND\xaeB`\x82'
        )
        image = SimpleUploadedFile('api_test.png', image_data, content_type='image/png')
        response = self.client.post(
            f'/api/ideas/{self.idea.pk}/upload-image/',
            {'image': image, 'caption': 'API uploaded'},
            format='multipart'
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(self.idea.images.count(), 1)

    def test_upload_image_no_file(self):
        """Test uploading with no image file."""
        response = self.client.post(
            f'/api/ideas/{self.idea.pk}/upload-image/',
            {'caption': 'No image'},
            format='multipart'
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_list_images(self):
        """Test listing all images."""
        response = self.client.get('/api/images/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_image(self):
        """Test deleting an image via API."""
        image_data = (
            b'\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR'
            b'\x00\x00\x00\x01\x00\x00\x00\x01\x08\x02'
            b'\x00\x00\x00\x90wS\xde\x00\x00\x00\x0c'
            b'IDATx\x9cc\xf8\x0f\x00\x00\x01\x01\x00'
            b'\x05\x18\xd8N\x00\x00\x00\x00IEND\xaeB`\x82'
        )
        img = IdeaImage.objects.create(
            idea=self.idea,
            image=SimpleUploadedFile('del.png', image_data, content_type='image/png')
        )
        response = self.client.delete(f'/api/images/{img.pk}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(IdeaImage.objects.filter(pk=img.pk).exists())
