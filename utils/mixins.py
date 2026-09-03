from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import AccessMixin
from django.shortcuts import redirect, get_object_or_404

from photos.models import Photo


User = get_user_model()


class AnonymousRequiredMixin(AccessMixin):
    """Verify that the current user is anonymous."""

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_anonymous:
            return redirect('photos:photos')
        return super().dispatch(request, *args, **kwargs)


class SelfForbiddenMixin:
    def dispatch(self, request, *args, **kwargs):
        user = get_object_or_404(User, username=kwargs['username'])

        if request.user == user:
            return redirect('photos:photos')
        return super().dispatch(request, *args, **kwargs)


class OwnerRequiredMixin:
    def dispatch(self, request, *args, **kwargs):
        user = get_object_or_404(User, username=kwargs['username'])

        if request.user != user:
            return redirect('photos:photos')
        return super().dispatch(request, *args, **kwargs)


class PhotoOwnerRequiredMixin:
    def dispatch(self, request, *args, **kwargs):
        photo = get_object_or_404(Photo, slug=kwargs['slug'])

        if request.user != photo.user:
            return redirect('photos:photos')
        return super().dispatch(request, *args, **kwargs)
