"""
Custom template filters for the Ideas app.
"""
import re
from django import template
from django.utils.safestring import mark_safe
from django.utils.html import escape

register = template.Library()


@register.filter(name='linkify')
def linkify(text):
    """
    Convert URLs in text to clickable links.
    Escapes HTML first for security, then wraps URLs in <a> tags.
    """
    if not text:
        return text

    # Escape HTML to prevent XSS
    escaped = escape(text)

    # Match URLs (http, https, ftp, and www.)
    url_pattern = re.compile(
        r'(https?://[^\s<>"\']+|www\.[^\s<>"\']+)',
        re.IGNORECASE
    )

    def replace_url(match):
        url = match.group(0)
        href = url if url.startswith(('http://', 'https://')) else f'https://{url}'
        return (
            f'<a href="{href}" target="_blank" rel="noopener noreferrer" '
            f'class="text-amber-700 underline hover:text-amber-900 transition-colors">'
            f'{url}</a>'
        )

    result = url_pattern.sub(replace_url, escaped)
    return mark_safe(result)


@register.filter(name='truncate_words_smart')
def truncate_words_smart(text, num_words=20):
    """Truncate text to a number of words, adding ellipsis if needed."""
    if not text:
        return text
    words = text.split()
    if len(words) <= num_words:
        return text
    return ' '.join(words[:num_words]) + '...'
