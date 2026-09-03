from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.views import View

from utils.mixins import AnonymousRequiredMixin


User = get_user_model()


class UserRegisterView(AnonymousRequiredMixin, View):
    template_name = 'accounts/register.html'

    def get(self, request):
        return render(request, self.template_name)


class UserLoginView(AnonymousRequiredMixin, View):
    template_name = 'accounts/login.html'

    def get(self, request):
        return render(request, self.template_name)


class UserLogoutView(LoginRequiredMixin, View):
    def get(self, request): pass


class UserForgotPasswordView(AnonymousRequiredMixin, View):
    template_name = 'accounts/forgot_password.html'

    def get(self, request):
        return render(request, self.template_name)


class UserVerifyCodeView(AnonymousRequiredMixin, View):
    template_name = 'accounts/verify_code.html'

    def get(self, request):
        return render(request, self.template_name)


class UserResetPasswordView(AnonymousRequiredMixin, View):
    template_name = 'accounts/reset_password.html'

    def get(self, request):
        return render(request, self.template_name)


class UserProfileView(LoginRequiredMixin, View):
    template_name = 'accounts/profile.html'

    def get(self, request):
        return render(request, self.template_name)


class UserProfileAboutView(LoginRequiredMixin, View):
    template_name = 'accounts/profile_about.html'

    def get(self, request):
        return render(request, self.template_name)


class UserSavedPhotosView(LoginRequiredMixin, View):
    template_name = 'accounts/profile_saved.html'

    def get(self, request):
        return render(request, self.template_name)


class UserEditProfileView(LoginRequiredMixin, View):
    template_name = 'accounts/edit_profile.html'

    def get(self, request):
        return render(request, self.template_name)


class UserDeleteAccountView(LoginRequiredMixin, View):
    template_name = 'accounts/delete_account.html'

    def get(self, request):
        return render(request, self.template_name)


class UserFollowView(LoginRequiredMixin, View):
    def get(self, request): pass


class UserUnfollowView(LoginRequiredMixin, View):
    def get(self, request): pass
