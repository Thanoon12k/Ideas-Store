"""
URL patterns for the Ideas app.
"""
from django.urls import path
from . import views

urlpatterns = [
    path('', views.idea_create, name='idea_create'),
    path('ideas/', views.idea_list, name='idea_list'),
    path('ideas/<int:pk>/', views.idea_detail, name='idea_detail'),
    path('ideas/<int:pk>/edit/', views.idea_edit, name='idea_edit'),
    path('ideas/<int:pk>/delete/', views.idea_delete, name='idea_delete'),
    path('ideas/image/<int:pk>/delete/', views.idea_image_delete, name='idea_image_delete'),
]
