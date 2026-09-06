from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.shortcuts import render, redirect, get_object_or_404
from django.views import View

from utils.mixins import PhotoOwnerRequiredMixin
from utils.pagination import get_pagination_context
from .models import Tag, Photo, Like, Save
from .forms import PhotoUploadForm


class PhotosView(View):
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
    form_class = PhotoUploadForm

    def get(self, request):
        form = self.form_class()
        tags = list(Tag.objects.values_list('name', flat=True))
        
        return render(request, self.template_name, {
            'form': form,
            'tags': tags,
        })

    def post(self, request):
        form = self.form_class(request.POST, request.FILES)
        
        if not form.is_valid():
            tags = list(Tag.objects.values_list('name', flat=True))
            return render(request, self.template_name, {
                'form': form,
                'tags': tags,
            })
        
        photo = form.save(request.user)
        return redirect(photo.get_absolute_url())


class PhotoDeleteView(LoginRequiredMixin, PhotoOwnerRequiredMixin, View):
    def get(self, request, **kwargs):
        get_object_or_404(Photo, slug=kwargs['slug']).delete()

        next_url = request.POST.get('next') or request.GET.get('next')
        return redirect(next_url or request.user.get_profile_url())


class PhotoLikeView(LoginRequiredMixin, View):
    def get(self, request, **kwargs):
        photo = get_object_or_404(Photo, slug=kwargs['slug'])

        if not Like.objects.filter(photo=photo, user=request.user).exists():
            Like.objects.create(photo=photo, user=request.user)
        
        next_url = request.POST.get('next') or request.GET.get('next')
        return redirect(next_url or photo.get_absolute_url())


class PhotoUnlikeView(LoginRequiredMixin, View):
    def get(self, request, **kwargs):
        photo = get_object_or_404(Photo, slug=kwargs['slug'])
        like = Like.objects.filter(photo=photo, user=request.user)

        if like.exists():
            like.delete()
        
        next_url = request.POST.get('next') or request.GET.get('next')
        return redirect(next_url or photo.get_absolute_url())


class PhotoSaveView(LoginRequiredMixin, View):
    def get(self, request, **kwargs):
        photo = get_object_or_404(Photo, slug=kwargs['slug'])

        if not Save.objects.filter(user=request.user, photo=photo).exists():
            Save.objects.create(user=request.user, photo=photo)

        next_url = request.POST.get('next') or request.GET.get('next')
        return redirect(next_url or photo.get_absolute_url())


class PhotoUnsaveView(LoginRequiredMixin, View):
    def get(self, request, **kwargs):
        photo = get_object_or_404(Photo, slug=kwargs['slug'])
        save = Save.objects.filter(user=request.user, photo=photo)

        if save.exists():
            save.delete()
        
        next_url = request.POST.get('next') or request.GET.get('next')
        return redirect(next_url or photo.get_absolute_url())
