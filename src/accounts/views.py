from django.contrib import messages
from django.contrib.auth import get_user_model, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect, get_object_or_404
from django.views import View

from utils.mixins import AnonymousRequiredMixin, SelfForbiddenMixin, OwnerRequiredMixin
from utils.pagination import get_pagination_context
from .models import Relation
from .forms import UserRegisterForm, UserLoginForm, UserEditProfileForm, UserDeleteAccountForm


User = get_user_model()


class UserRegisterView(AnonymousRequiredMixin, View):
    template_name = 'accounts/register.html'
    form_class = UserRegisterForm

    def get(self, request):
        return render(request, self.template_name, {'form': self.form_class()})

    def post(self, request):
        form = self.form_class(request.POST)

        if not form.is_valid():
            return render(request, self.template_name, {'form': form})

        form.save()
        # messages.success(request, 'Account created successfully. Please sign in.', 'success')
        return redirect('accounts:user-login')


class UserLoginView(AnonymousRequiredMixin, View):
    template_name = 'accounts/login.html'
    form_class = UserLoginForm

    def get(self, request):
        return render(request, self.template_name, {'form': self.form_class()})

    def post(self, request):
        form = self.form_class(request.POST)

        if not form.is_valid():
            return render(request, self.template_name, {'form': form})

        user = form.user
        login(request, user)

        # messages.success(request, 'Logged in successfully.', 'success')

        return redirect(request.GET.get('next') or 'photos:photos')


class UserLogoutView(LoginRequiredMixin, View):
    def get(self, request):
        logout(request)
        return redirect('photos:photos')


class UserProfileView(View):
    template_name = 'accounts/profile.html'

    def get(self, request, **kwargs):
        user = get_object_or_404(User, username=kwargs['username'])
        return render(request, self.template_name, {
            'user': user,
            'page_obj': get_pagination_context(request, user.get_photos(), 20),
        })


class UserProfileAboutView(View):
    template_name = 'accounts/profile_about.html'

    def get(self, request, **kwargs):
        user = get_object_or_404(User, username=kwargs['username'])
        return render(request, self.template_name, {
            'user': user,
        })


class UserSavedPhotosView(LoginRequiredMixin, View):
    template_name = 'accounts/profile_saved.html'

    def get(self, request, **kwargs):
        user = get_object_or_404(User, username=kwargs['username'])
        return render(request, self.template_name, {
            'user': user,
            'page_obj': get_pagination_context(request, user.get_saved_photos(), 20),
        })


class UserEditProfileView(LoginRequiredMixin, OwnerRequiredMixin, View):
    template_name = 'accounts/edit_profile.html'
    form_class = UserEditProfileForm

    def setup(self, request, *args, **kwargs):
        self.user_instance = get_object_or_404(User, username=kwargs['username'])
        return super().setup(request, *args, **kwargs)

    def get(self, request, **kwargs):
        user = self.user_instance
        return render(request, self.template_name, {
            'form': self.form_class(initial={
                'username': user.username,
                'email': user.email,
                'full_name': user.full_name,
                'bio': user.bio,
            }, user=user),
        })

    def post(self, request, **kwargs):
        user = self.user_instance
        form = self.form_class(request.POST, request.FILES, user=user)

        if not form.is_valid():
            return render(request, self.template_name, {'form': form})

        form.save()
        return redirect('accounts:user-profile', username=user.username)


class UserDeleteAvatarView(LoginRequiredMixin, OwnerRequiredMixin, View):
    def get(self, request, **kwargs):
        user = get_object_or_404(User, username=kwargs['username'])

        if user.avatar:
            user.avatar.delete()

        return redirect(user.get_edit_profile_url())


class UserDeleteAccountView(LoginRequiredMixin, OwnerRequiredMixin, View):
    template_name = 'accounts/delete_account.html'
    form_class = UserDeleteAccountForm

    def get(self, request, **kwargs):
        return render(request, self.template_name, {'form': self.form_class()})

    def post(self, request, **kwargs):
        form = self.form_class(request.POST, user=request.user)

        if not form.is_valid():
            return render(request, self.template_name, {'form': form})

        form.save()
        return redirect('photos:photos')


class UserFollowView(LoginRequiredMixin, SelfForbiddenMixin, View):
    def get(self, request, **kwargs):
        user = get_object_or_404(User, username=kwargs['username'])

        if not Relation.objects.filter(from_user=request.user, to_user=user).exists():
            Relation.objects.create(from_user=request.user, to_user=user)

        return redirect(user.get_profile_url())


class UserUnfollowView(LoginRequiredMixin, SelfForbiddenMixin, View):
    def get(self, request, **kwargs):
        user = get_object_or_404(User, username=kwargs['username'])
        relation = Relation.objects.filter(from_user=request.user, to_user=user)
        
        if relation:
            relation.delete()

        return redirect(user.get_profile_url())
