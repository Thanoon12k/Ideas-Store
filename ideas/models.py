"""
Models for the Ideas Store application.
"""
from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _


class Idea(models.Model):
    """Represents a single idea with optional voice note."""
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='ideas',
        verbose_name=_('User')
    )
    title = models.CharField(
        _('Title'),
        max_length=200,
        help_text=_('Give your idea a short, descriptive title.')
    )
    description = models.TextField(
        _('Description'),
        blank=True,
        help_text=_('Describe your idea in detail. URLs will be auto-linked.')
    )
    voice_note = models.FileField(
        _('Voice Note'),
        upload_to='voices/%Y/%m/',
        blank=True,
        null=True,
        help_text=_('Record or upload a voice note for this idea.')
    )
    created_at = models.DateTimeField(_('Created'), auto_now_add=True)
    updated_at = models.DateTimeField(_('Updated'), auto_now=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = _('Idea')
        verbose_name_plural = _('Ideas')

    def __str__(self):
        return self.title


class IdeaImage(models.Model):
    """An image attached to an idea. Supports multiple images per idea."""
    idea = models.ForeignKey(
        Idea,
        on_delete=models.CASCADE,
        related_name='images',
        verbose_name=_('Idea')
    )
    image = models.ImageField(
        _('Image'),
        upload_to='idea_images/%Y/%m/'
    )
    caption = models.CharField(
        _('Caption'),
        max_length=200,
        blank=True
    )
    uploaded_at = models.DateTimeField(_('Uploaded'), auto_now_add=True)

    class Meta:
        ordering = ['uploaded_at']
        verbose_name = _('Idea Image')
        verbose_name_plural = _('Idea Images')

    def __str__(self):
        return f"{self.idea.title} - Image {self.pk}"
