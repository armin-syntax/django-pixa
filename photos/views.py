from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.shortcuts import render, get_object_or_404
from django.views import View

from utils.pagination import get_pagination_context
from .models import Tag, Photo


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
    def get(self, request): pass


class PhotoUnlikeView(LoginRequiredMixin, View):
    def get(self, request): pass


class PhotoSaveView(LoginRequiredMixin, View):
    def get(self, request): pass


class PhotoUnsaveView(LoginRequiredMixin, View):
    def get(self, request): pass
