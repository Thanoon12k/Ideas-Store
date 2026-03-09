"""
Views for the Ideas Store application.
"""
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils.translation import gettext_lazy as _
from .models import Idea, IdeaImage
from .forms import IdeaForm


@login_required
def idea_create(request):
    """Main landing page — create a new idea with voice and images."""
    if request.method == 'POST':
        form = IdeaForm(request.POST, request.FILES)
        if form.is_valid():
            idea = form.save(commit=False)
            idea.user = request.user
            idea.save()

            # Handle multiple image uploads
            images = request.FILES.getlist('images')
            for image_file in images:
                if image_file.size <= 5 * 1024 * 1024:  # 5MB limit per image
                    IdeaImage.objects.create(idea=idea, image=image_file)

            messages.success(request, _('Your idea has been saved! 💡'))
            return redirect('idea_list')
    else:
        form = IdeaForm()

    return render(request, 'ideas/idea_form.html', {'form': form})


@login_required
def idea_list(request):
    """Browse all saved ideas, newest first."""
    ideas = Idea.objects.prefetch_related('images').filter(user=request.user)
    return render(request, 'ideas/idea_list.html', {'ideas': ideas})


@login_required
def idea_detail(request, pk):
    """View a single idea with all its media."""
    idea = get_object_or_404(Idea.objects.prefetch_related('images'), pk=pk, user=request.user)
    return render(request, 'ideas/idea_detail.html', {'idea': idea})


@login_required
def idea_delete(request, pk):
    """Delete an idea with confirmation."""
    idea = get_object_or_404(Idea, pk=pk, user=request.user)
    if request.method == 'POST':
        idea.delete()
        messages.success(request, _('Idea deleted.'))
        return redirect('idea_list')
    return render(request, 'ideas/idea_confirm_delete.html', {'idea': idea})


@login_required
def idea_edit(request, pk):
    """Edit an existing idea."""
    idea = get_object_or_404(Idea, pk=pk, user=request.user)
    if request.method == 'POST':
        form = IdeaForm(request.POST, request.FILES, instance=idea)
        if form.is_valid():
            idea = form.save()

            # Handle new image uploads
            images = request.FILES.getlist('images')
            for image_file in images:
                if image_file.size <= 5 * 1024 * 1024:
                    IdeaImage.objects.create(idea=idea, image=image_file)

            messages.success(request, _('Idea updated! 💡'))
            return redirect('idea_detail', pk=idea.pk)
    else:
        form = IdeaForm(instance=idea)

    return render(request, 'ideas/idea_form.html', {
        'form': form,
        'idea': idea,
        'editing': True,
    })


@login_required
def idea_image_delete(request, pk):
    """Delete a single image from an idea."""
    image = get_object_or_404(IdeaImage, pk=pk, idea__user=request.user)
    idea_pk = image.idea.pk
    if request.method == 'POST':
        image.delete()
        messages.success(request, _('Image removed.'))
    return redirect('idea_detail', pk=idea_pk)
