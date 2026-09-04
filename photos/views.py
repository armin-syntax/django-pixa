from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.shortcuts import render, redirect, get_object_or_404
from django.views import View

from utils.pagination import get_pagination_context
from .models import Tag, Photo, Like, Save


class PhotoListView(View):
    template_name = 'photos/index.html'

    def get(self, request):
        tags = Tag.objects.all()[:5]
        photos = Photo.objects.all()

        if request.GET.get('search'):
            search = request.GET['search']
            photos = photos.filter(
                Q(title__icontains=search) |
                Q(slug__icontains=search) |
                Q(caption__icontains=search) |
                Q(tags__name__icontains=search) |
                Q(user__username__icontains=search) |
                Q(user__full_name__icontains=search)
            )

        if request.GET.get('tag'):
            selected_tag = request.GET['tag']
            photos = photos.filter(tags__slug=selected_tag)

        return render(request, self.template_name, {
            'tags': tags,
            'page_obj': get_pagination_context(request, photos, 20),
        })


class TagListView(View):
    template_name = 'photos/tags.html'

    def get(self, request):
        tags = Tag.objects.all()
        return render(request, self.template_name, {
            'tags': tags,
        })


class PhotoDetailView(View):
    template_name = 'photos/photo.html'

    def get(self, request, **kwargs):
        photo = get_object_or_404(Photo, slug=kwargs['slug'])
        return render(request, self.template_name, {
            'photo': photo,
        })


class PhotoUploadView(LoginRequiredMixin, View):
    template_name = 'photos/upload.html'

    def get(self, request):
        return render(request, self.template_name)


class PhotoDeleteView(LoginRequiredMixin, View):
    def get(self, request): pass


class PhotoLikeView(LoginRequiredMixin, View):
    def get(self, request, **kwargs):
        photo = get_object_or_404(Photo, slug=kwargs['slug'])

        if not Like.objects.filter(photo=photo, user=request.user).exists():
            Like.objects.create(photo=photo, user=request.user)
            # messages.success(request, 'Photo liked successfully', 'success')
        
        return redirect(photo.get_absolute_url())


class PhotoUnlikeView(LoginRequiredMixin, View):
    def get(self, request, **kwargs):
        photo = get_object_or_404(Photo, slug=kwargs['slug'])
        like = Like.objects.filter(photo=photo, user=request.user)

        if like.exists():
            like.delete()
            # messages.success(request, 'Photo unliked successfully', 'success')
        
        return redirect(photo.get_absolute_url())


class PhotoSaveView(LoginRequiredMixin, View):
    def get(self, request, **kwargs):
        photo = get_object_or_404(Photo, slug=kwargs['slug'])

        if not Save.objects.filter(user=request.user, photo=photo).exists():
            Save.objects.create(user=request.user, photo=photo)
            # messages.success(request, 'Photo saved successfully', 'success')
        
        return redirect(photo.get_absolute_url())


class PhotoUnsaveView(LoginRequiredMixin, View):
    def get(self, request, **kwargs):
        photo = get_object_or_404(Photo, slug=kwargs['slug'])
        save = Save.objects.filter(user=request.user, photo=photo)

        if save.exists():
            save.delete()
            # messages.success(request, 'Photo unsaved successfully', 'success')
        
        return redirect(photo.get_absolute_url())
