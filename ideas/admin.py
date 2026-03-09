"""
Admin configuration for the Ideas Store application.
"""
from django.contrib import admin
from .models import Idea, IdeaImage


class IdeaImageInline(admin.TabularInline):
    model = IdeaImage
    extra = 1


@admin.register(Idea)
class IdeaAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'created_at', 'updated_at')
    list_filter = ('created_at', 'user')
    search_fields = ('title', 'description')
    inlines = [IdeaImageInline]
    readonly_fields = ('created_at', 'updated_at')


@admin.register(IdeaImage)
class IdeaImageAdmin(admin.ModelAdmin):
    list_display = ('idea', 'caption', 'uploaded_at')
    list_filter = ('uploaded_at',)
