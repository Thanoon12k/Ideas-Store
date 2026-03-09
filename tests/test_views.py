"""
Tests for Ideas Store views.
"""
from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from django.core.files.uploadedfile import SimpleUploadedFile
from ideas.models import Idea, IdeaImage


class ViewTestBase(TestCase):
    """Base test class with common setup."""

    def setUp(self):
        """Create test user and client."""
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123!'
        )
        self.client.login(username='testuser', password='testpass123!')

        self.idea = Idea.objects.create(
            user=self.user,
            title='Test Idea',
            description='Test description with https://example.com link'
        )


class IdeaCreateViewTest(ViewTestBase):
    """Tests for the idea creation view (main landing page)."""

    def test_create_page_loads(self):
        """Test that the create page loads successfully."""
        response = self.client.get(reverse('idea_create'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'ideas/idea_form.html')

    def test_create_page_contains_form(self):
        """Test that the form is present."""
        response = self.client.get(reverse('idea_create'))
        self.assertContains(response, 'id="idea-form"')

    def test_create_idea_post(self):
        """Test creating an idea via POST."""
        response = self.client.post(reverse('idea_create'), {
            'title': 'New Idea',
            'description': 'New description',
        })
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Idea.objects.filter(title='New Idea').exists())

    def test_create_idea_with_images(self):
        """Test creating an idea with images."""
        image_data = (
            b'\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR'
            b'\x00\x00\x00\x01\x00\x00\x00\x01\x08\x02'
            b'\x00\x00\x00\x90wS\xde\x00\x00\x00\x0c'
            b'IDATx\x9cc\xf8\x0f\x00\x00\x01\x01\x00'
            b'\x05\x18\xd8N\x00\x00\x00\x00IEND\xaeB`\x82'
        )
        image = SimpleUploadedFile('test.png', image_data, content_type='image/png')
        response = self.client.post(reverse('idea_create'), {
            'title': 'Idea with Image',
            'description': 'Has an image',
            'images': [image],
        })
        self.assertEqual(response.status_code, 302)
        idea = Idea.objects.get(title='Idea with Image')
        self.assertEqual(idea.images.count(), 1)

    def test_create_idea_empty_title(self):
        """Test that title is required."""
        response = self.client.post(reverse('idea_create'), {
            'title': '',
            'description': 'No title',
        })
        self.assertEqual(response.status_code, 200)  # Form re-rendered with errors

    def test_redirect_when_not_logged_in(self):
        """Test that unauthenticated users are redirected."""
        self.client.logout()
        response = self.client.get(reverse('idea_create'))
        self.assertEqual(response.status_code, 302)
        self.assertIn('/login/', response.url)


class IdeaListViewTest(ViewTestBase):
    """Tests for the ideas list view."""

    def test_list_page_loads(self):
        """Test that the list page loads."""
        response = self.client.get(reverse('idea_list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'ideas/idea_list.html')

    def test_list_contains_idea(self):
        """Test that the list contains the test idea."""
        response = self.client.get(reverse('idea_list'))
        self.assertContains(response, 'Test Idea')

    def test_list_empty(self):
        """Test empty state message."""
        Idea.objects.all().delete()
        response = self.client.get(reverse('idea_list'))
        self.assertEqual(response.status_code, 200)


class IdeaDetailViewTest(ViewTestBase):
    """Tests for the idea detail view."""

    def test_detail_page_loads(self):
        """Test that the detail page loads."""
        response = self.client.get(reverse('idea_detail', args=[self.idea.pk]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'ideas/idea_detail.html')

    def test_detail_contains_title(self):
        """Test that the detail page shows the idea title."""
        response = self.client.get(reverse('idea_detail', args=[self.idea.pk]))
        self.assertContains(response, 'Test Idea')

    def test_detail_404(self):
        """Test 404 for non-existent idea."""
        response = self.client.get(reverse('idea_detail', args=[99999]))
        self.assertEqual(response.status_code, 404)


class IdeaDeleteViewTest(ViewTestBase):
    """Tests for the idea delete view."""

    def test_delete_confirm_page(self):
        """Test delete confirmation page loads."""
        response = self.client.get(reverse('idea_delete', args=[self.idea.pk]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'ideas/idea_confirm_delete.html')

    def test_delete_idea(self):
        """Test deleting an idea via POST."""
        pk = self.idea.pk
        response = self.client.post(reverse('idea_delete', args=[pk]))
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Idea.objects.filter(pk=pk).exists())


class IdeaEditViewTest(ViewTestBase):
    """Tests for the idea edit view."""

    def test_edit_page_loads(self):
        """Test that the edit page loads with existing data."""
        response = self.client.get(reverse('idea_edit', args=[self.idea.pk]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Idea')

    def test_edit_idea_post(self):
        """Test updating an idea."""
        response = self.client.post(reverse('idea_edit', args=[self.idea.pk]), {
            'title': 'Updated Title',
            'description': 'Updated description',
        })
        self.assertEqual(response.status_code, 302)
        self.idea.refresh_from_db()
        self.assertEqual(self.idea.title, 'Updated Title')


class IdeaImageDeleteViewTest(ViewTestBase):
    """Tests for image deletion."""

    def setUp(self):
        super().setUp()
        image_data = (
            b'\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR'
            b'\x00\x00\x00\x01\x00\x00\x00\x01\x08\x02'
            b'\x00\x00\x00\x90wS\xde\x00\x00\x00\x0c'
            b'IDATx\x9cc\xf8\x0f\x00\x00\x01\x01\x00'
            b'\x05\x18\xd8N\x00\x00\x00\x00IEND\xaeB`\x82'
        )
        self.image = IdeaImage.objects.create(
            idea=self.idea,
            image=SimpleUploadedFile('test.png', image_data, content_type='image/png')
        )

    def test_delete_image(self):
        """Test deleting an image."""
        pk = self.image.pk
        response = self.client.post(reverse('idea_image_delete', args=[pk]))
        self.assertEqual(response.status_code, 302)
        self.assertFalse(IdeaImage.objects.filter(pk=pk).exists())
