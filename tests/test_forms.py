"""
Tests for Ideas Store forms.
"""
from io import BytesIO
from PIL import Image as PILImage
from django.test import TestCase
from django.core.files.uploadedfile import SimpleUploadedFile
from ideas.forms import IdeaForm, IdeaImageForm


def create_test_image(name='test.png', size=(1, 1), fmt='PNG'):
    """Create a valid in-memory image for testing."""
    buffer = BytesIO()
    img = PILImage.new('RGB', size, color='red')
    img.save(buffer, format=fmt)
    buffer.seek(0)
    return SimpleUploadedFile(name, buffer.read(), content_type=f'image/{fmt.lower()}')


class IdeaFormTest(TestCase):
    """Tests for the IdeaForm."""

    def test_valid_form(self):
        """Test form with valid data."""
        form = IdeaForm(data={
            'title': 'Test Idea',
            'description': 'A great idea',
        })
        self.assertTrue(form.is_valid())

    def test_empty_title(self):
        """Test that title is required."""
        form = IdeaForm(data={
            'title': '',
            'description': 'No title',
        })
        self.assertFalse(form.is_valid())
        self.assertIn('title', form.errors)

    def test_title_max_length(self):
        """Test title max length validation."""
        form = IdeaForm(data={
            'title': 'x' * 201,  # Exceeds max_length=200
            'description': 'Long title',
        })
        self.assertFalse(form.is_valid())
        self.assertIn('title', form.errors)

    def test_blank_description(self):
        """Test that description can be blank."""
        form = IdeaForm(data={
            'title': 'Title Only',
            'description': '',
        })
        self.assertTrue(form.is_valid())

    def test_voice_note_size_limit(self):
        """Test voice note max 10MB."""
        large_file = SimpleUploadedFile(
            'large.webm',
            b'x' * (11 * 1024 * 1024),  # 11MB
            content_type='audio/webm'
        )
        form = IdeaForm(data={'title': 'Test'}, files={'voice_note': large_file})
        self.assertFalse(form.is_valid())
        self.assertIn('voice_note', form.errors)

    def test_valid_voice_note(self):
        """Test form with valid voice file."""
        audio = SimpleUploadedFile(
            'voice.webm',
            b'\x00\x01\x02\x03',
            content_type='audio/webm'
        )
        form = IdeaForm(
            data={'title': 'Voice Idea', 'description': ''},
            files={'voice_note': audio}
        )
        self.assertTrue(form.is_valid())


class IdeaImageFormTest(TestCase):
    """Tests for the IdeaImageForm."""

    def test_valid_image(self):
        """Test form with valid image."""
        image = create_test_image('test.png')
        form = IdeaImageForm(data={'caption': 'Cap'}, files={'image': image})
        self.assertTrue(form.is_valid())

    def test_image_size_limit(self):
        """Test image max 5MB."""
        large_image = SimpleUploadedFile(
            'large.png',
            b'x' * (6 * 1024 * 1024),  # 6MB
            content_type='image/png'
        )
        form = IdeaImageForm(data={'caption': ''}, files={'image': large_image})
        self.assertFalse(form.is_valid())
        self.assertIn('image', form.errors)

    def test_blank_caption(self):
        """Test that caption can be blank."""
        image = create_test_image('test2.png')
        form = IdeaImageForm(data={'caption': ''}, files={'image': image})
        self.assertTrue(form.is_valid())
