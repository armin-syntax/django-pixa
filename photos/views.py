from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.views import View


class PhotoListView(View):
    template_name = 'photos/index.html'

    def get(self, request):
        return render(request, self.template_name)


class TagListView(View):
    template_name = 'photos/tags.html'

    def get(self, request):
        return render(request, self.template_name)


class PhotoDetailView(View):
    template_name = 'photos/photo_detail.html'

    def get(self, request):
        return render(request, self.template_name)


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
