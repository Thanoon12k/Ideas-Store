"""
Tests for Ideas Store models.
"""
from django.test import TestCase
from django.core.files.uploadedfile import SimpleUploadedFile
from ideas.models import Idea, IdeaImage


class IdeaModelTest(TestCase):
    """Tests for the Idea model."""

    def setUp(self):
        """Create a test idea."""
        self.idea = Idea.objects.create(
            title='Test Idea',
            description='This is a test idea with a link https://example.com'
        )

    def test_idea_creation(self):
        """Test that an idea is created correctly."""
        self.assertEqual(self.idea.title, 'Test Idea')
        self.assertEqual(self.idea.description, 'This is a test idea with a link https://example.com')
        self.assertIsNotNone(self.idea.created_at)
        self.assertIsNotNone(self.idea.updated_at)

    def test_idea_str(self):
        """Test string representation of an idea."""
        self.assertEqual(str(self.idea), 'Test Idea')

    def test_idea_ordering(self):
        """Test that ideas are ordered by newest first (by created_at desc)."""
        import time
        time.sleep(0.1)  # Ensure different timestamps
        idea2 = Idea.objects.create(title='Second Idea')
        ideas = list(Idea.objects.all())
        # idea2 was created later, should appear first
        self.assertEqual(ideas[0].title, 'Second Idea')
        self.assertEqual(ideas[1].title, 'Test Idea')

    def test_idea_blank_fields(self):
        """Test that voice_note and description can be blank."""
        idea = Idea.objects.create(title='Minimal Idea')
        self.assertEqual(idea.description, '')
        self.assertFalse(idea.voice_note)

    def test_idea_with_voice_note(self):
        """Test creating an idea with a voice note."""
        audio_content = b'\x00\x01\x02\x03'  # Dummy audio data
        voice = SimpleUploadedFile('test_voice.webm', audio_content, content_type='audio/webm')
        idea = Idea.objects.create(
            title='Voice Idea',
            voice_note=voice
        )
        self.assertTrue(idea.voice_note)
        self.assertIn('voices/', idea.voice_note.name)

    def test_idea_update(self):
        """Test updating an idea."""
        self.idea.title = 'Updated Title'
        self.idea.save()
        self.idea.refresh_from_db()
        self.assertEqual(self.idea.title, 'Updated Title')


class IdeaImageModelTest(TestCase):
    """Tests for the IdeaImage model."""

    def setUp(self):
        """Create a test idea and image."""
        self.idea = Idea.objects.create(title='Test Idea')
        image_data = (
            b'\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR'
            b'\x00\x00\x00\x01\x00\x00\x00\x01\x08\x02'
            b'\x00\x00\x00\x90wS\xde\x00\x00\x00\x0c'
            b'IDATx\x9cc\xf8\x0f\x00\x00\x01\x01\x00'
            b'\x05\x18\xd8N\x00\x00\x00\x00IEND\xaeB`\x82'
        )
        self.image = IdeaImage.objects.create(
            idea=self.idea,
            image=SimpleUploadedFile('test.png', image_data, content_type='image/png'),
            caption='Test Caption'
        )

    def test_image_creation(self):
        """Test image creation and relationship."""
        self.assertEqual(self.image.idea, self.idea)
        self.assertEqual(self.image.caption, 'Test Caption')
        self.assertTrue(self.image.image)

    def test_image_str(self):
        """Test string representation of an image."""
        self.assertIn('Test Idea', str(self.image))

    def test_image_idea_relationship(self):
        """Test that images are accessible via idea.images."""
        self.assertEqual(self.idea.images.count(), 1)
        self.assertEqual(self.idea.images.first(), self.image)

    def test_cascade_delete(self):
        """Test that deleting an idea also deletes its images."""
        idea_pk = self.idea.pk
        image_pk = self.image.pk
        self.idea.delete()
        self.assertEqual(IdeaImage.objects.filter(pk=image_pk).count(), 0)
        self.assertEqual(Idea.objects.filter(pk=idea_pk).count(), 0)

    def test_multiple_images(self):
        """Test multiple images per idea."""
        image_data = (
            b'\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR'
            b'\x00\x00\x00\x01\x00\x00\x00\x01\x08\x02'
            b'\x00\x00\x00\x90wS\xde\x00\x00\x00\x0c'
            b'IDATx\x9cc\xf8\x0f\x00\x00\x01\x01\x00'
            b'\x05\x18\xd8N\x00\x00\x00\x00IEND\xaeB`\x82'
        )
        IdeaImage.objects.create(
            idea=self.idea,
            image=SimpleUploadedFile('test2.png', image_data, content_type='image/png')
        )
        self.assertEqual(self.idea.images.count(), 2)

    def test_blank_caption(self):
        """Test that caption can be blank."""
        image_data = (
            b'\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR'
            b'\x00\x00\x00\x01\x00\x00\x00\x01\x08\x02'
            b'\x00\x00\x00\x90wS\xde\x00\x00\x00\x0c'
            b'IDATx\x9cc\xf8\x0f\x00\x00\x01\x01\x00'
            b'\x05\x18\xd8N\x00\x00\x00\x00IEND\xaeB`\x82'
        )
        img = IdeaImage.objects.create(
            idea=self.idea,
            image=SimpleUploadedFile('test3.png', image_data, content_type='image/png')
        )
        self.assertEqual(img.caption, '')
