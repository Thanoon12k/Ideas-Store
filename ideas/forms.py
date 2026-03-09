"""
Forms for the Ideas Store application.
"""
from django import forms
from django.utils.translation import gettext_lazy as _
from .models import Idea, IdeaImage


class IdeaForm(forms.ModelForm):
    """Form for creating and editing ideas."""

    class Meta:
        model = Idea
        fields = ['title', 'description', 'voice_note']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'w-full px-4 py-3 rounded-xl border border-stone-300 '
                         'bg-white/70 focus:outline-none focus:ring-2 '
                         'focus:ring-amber-400/50 focus:border-amber-400 '
                         'text-stone-800 placeholder-stone-400 transition-all',
                'placeholder': _('What\'s your idea?'),
                'autocomplete': 'off',
            }),
            'description': forms.Textarea(attrs={
                'class': 'w-full px-4 py-3 rounded-xl border border-stone-300 '
                         'bg-white/70 focus:outline-none focus:ring-2 '
                         'focus:ring-amber-400/50 focus:border-amber-400 '
                         'text-stone-800 placeholder-stone-400 transition-all resize-none',
                'placeholder': _('Describe your idea... (URLs will be clickable)'),
                'rows': 4,
            }),
            'voice_note': forms.ClearableFileInput(attrs={
                'class': 'hidden',
                'accept': 'audio/*',
                'id': 'voice-file-input',
            }),
        }

    def clean_voice_note(self):
        """Validate voice note file size (max 10MB)."""
        voice = self.cleaned_data.get('voice_note')
        if voice:
            if voice.size > 10 * 1024 * 1024:
                raise forms.ValidationError(
                    _('Voice note must be less than 10 MB.')
                )
        return voice


class IdeaImageForm(forms.ModelForm):
    """Form for uploading images to an idea."""

    class Meta:
        model = IdeaImage
        fields = ['image', 'caption']
        widgets = {
            'image': forms.ClearableFileInput(attrs={
                'class': 'hidden',
                'accept': 'image/*',
            }),
            'caption': forms.TextInput(attrs={
                'class': 'w-full px-3 py-2 rounded-lg border border-stone-300 '
                         'bg-white/70 text-stone-700 text-sm',
                'placeholder': _('Caption (optional)'),
            }),
        }

    def clean_image(self):
        """Validate image file size (max 5MB)."""
        image = self.cleaned_data.get('image')
        if image:
            if image.size > 5 * 1024 * 1024:
                raise forms.ValidationError(
                    _('Image must be less than 5 MB.')
                )
        return image
