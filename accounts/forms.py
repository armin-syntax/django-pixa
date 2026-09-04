from django import forms
from django.contrib.auth import get_user_model, authenticate
from django.core.exceptions import ValidationError
from django.core.validators import FileExtensionValidator

from utils.validators import UsernameValidator, NameValidator


User = get_user_model()


class UserBaseForm(forms.Form):
    username = forms.CharField(
        max_length=30,
        validators=[UsernameValidator()],
        widget=forms.TextInput(attrs={
            'placeholder': 'Choose a username',
            'class': 'field',
            'autocomplete': 'username',
        }),
    )
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={
            'placeholder': 'you@example.com',
            'class': 'field',
            'autocomplete': 'email',
        }),
    )
    full_name = forms.CharField(
        max_length=100,
        validators=[NameValidator('Full name')],
        widget=forms.TextInput(attrs={
            'placeholder': 'Enter your full name',
            'class': 'field',
            'autocomplete': 'name',
        }),
    )


class UserRegisterForm(UserBaseForm):
    password = forms.CharField(
        min_length=8,
        max_length=128,
        widget=forms.PasswordInput(attrs={
            'placeholder': 'Enter your password',
            'class': 'field',
            'autocomplete': 'new-password',
        }),
    )
    confirm_password = forms.CharField(
        min_length=8,
        max_length=128,
        widget=forms.PasswordInput(attrs={
            'placeholder': 'Confirm your password',
            'class': 'field',
            'autocomplete': 'new-password',
        }),
    )

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if username and User.objects.filter(username=username).exists():
            raise ValidationError('This username already exists.')
        return username

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if email and User.objects.filter(email=email).exists():
            raise ValidationError('This email address already exists.')
        return email

    def clean(self):
        cd = super().clean()
        password = cd.get('password')
        confirm_password = cd.get('confirm_password')

        if password and confirm_password and password != confirm_password:
            raise ValidationError('Passwords do not match.')
        return cd

    def save(self):
        cd = self.cleaned_data
        cd.pop('confirm_password')
        return User.objects.create_user(**cd)


class UserLoginForm(forms.Form):
    identity = forms.CharField(
        max_length=30,
        widget=forms.TextInput(attrs={
            'placeholder': 'Username or email',
            'class': 'field',
            'autocomplete': 'username',
        }),
    )
    password = forms.CharField(
        max_length=128,
        widget=forms.PasswordInput(attrs={
            'placeholder': 'Your password',
            'class': 'field',
            'autocomplete': 'current-password',
        }),
    )

    def clean(self):
        cd = super().clean()
        identity = cd.get('identity')
        password = cd.get('password')

        if identity and password:
            user = None

            if '@' in identity:
                try:
                    user_obj = User.objects.get(email=identity)
                    user = authenticate(username=user_obj.username, password=password)
                except User.DoesNotExist:
                    pass
            else:
                user = authenticate(username=identity, password=password)

            if user is None:
                raise ValidationError('Wrong username/email or password.')

            self.user = user

        return cd


class UserEditProfileForm(UserBaseForm):
    bio = forms.CharField(
        max_length=500,
        required=False,
        widget=forms.Textarea(attrs={
            'placeholder': 'Write a short bio...',
            'class': 'field',
            'rows': 5,
        }),
    )
    avatar = forms.ImageField(
        required=False,
        validators=[
            FileExtensionValidator(
                allowed_extensions=['png', 'jpg', 'jpeg'],
            ),
        ],
        widget=forms.FileInput(attrs={
            'class': 'field',
            'accept': 'image/*',
        }),
    )

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if username and User.objects.filter(username=username).exclude(pk=self.user.pk).exists():
            raise ValidationError('This username already exists.')
        return username

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if email and User.objects.filter(email=email).exclude(pk=self.user.pk).exists():
            raise ValidationError('This email address already exists.')
        return email

    def save(self):
        cd = self.cleaned_data

        self.user.username = cd['username']
        self.user.email = cd['email']
        self.user.full_name = cd['full_name']
        self.user.bio = cd.get('bio', '')

        if cd.get('avatar'):
            if self.user.avatar and self.user.avatar.path:
                import os
                try:
                    os.remove(self.user.avatar.path)
                except:
                    pass
            self.user.avatar = cd['avatar']

        self.user.save()
        return self.user
