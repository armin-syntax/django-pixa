from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.core.validators import FileExtensionValidator

from utils.paths import user_avatar_upload_path
from utils.validators import UsernameValidator, NameValidator
from utils.time import get_time_since


User = settings.AUTH_USER_MODEL


class CustomUser(AbstractUser):
    username = models.CharField(
        max_length=30,
        unique=True,
        validators=[UsernameValidator()],
        error_messages={
            'unique': 'This username already exists.',
        },
    )
    email = models.EmailField(
        unique=True,
        verbose_name='email address',
        error_messages={
            'unique': 'This email address already exists.',
        },
    )
    full_name = models.CharField(
        max_length=100,
        validators=[
            NameValidator(),
        ],
    )
    bio = models.TextField(max_length=200, blank=True, null=True)
    avatar = models.ImageField(
        upload_to=user_avatar_upload_path,
        blank=True,
        null=True,
        validators=[
            FileExtensionValidator(
                allowed_extensions=['png', 'jpg', 'jpeg',],
            ),
        ],
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    # I don`t need these fields
    first_name = None
    last_name = None

    class Meta:
        ordering = ['username']
        verbose_name = 'User'
        verbose_name_plural = 'Users'

    @property
    def created_since(self):
        return get_time_since(self.created_at)

    # ----- COUNTS -----

    @property
    def followers_count(self):
        return self.followers.count()

    @property
    def following_count(self):
        return self.following.count()

    @property
    def photos_count(self):
        return self.photos.count()

    # ----- LISTS -----

    def get_followers(self):
        return CustomUser.objects.filter(following__to_user=self)
    
    def get_following(self):
        return CustomUser.objects.filter(followers__from_user=self)

    def get_photos(self):
        return self.photos.all()


class Relation(models.Model):
    from_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='following')
    to_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='followers')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        unique_together = ['from_user', 'to_user']
    
    def __str__(self):
        return f'{self.from_user} followed {self.to_user}'

    @property
    def created_since(self):
        return get_time_since(self.created_at)
