import uuid

from django.db import models
from django.conf import settings
from django.urls import reverse
from django.utils.text import slugify
from django.core.validators import FileExtensionValidator

from utils.time import get_time_since
from utils.paths import photo_upload_path


User = settings.AUTH_USER_MODEL


class Tag(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=150, unique=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            generated_slug = f'{slugify(self.name)}-{uuid.uuid4()}'
            self.slug = generated_slug

        super().save(*args, **kwargs)

    @property
    def created_since(self):
        return get_time_since(self.created_at)


class Photo(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='photos')
    title = models.CharField(max_length=100)
    slug = models.SlugField(max_length=150, unique=True, blank=True)
    caption = models.TextField(max_length=200, blank=True, null=True)
    image = models.ImageField(
        upload_to=photo_upload_path,
        validators=[
            FileExtensionValidator(
                allowed_extensions=['png', 'jpg', 'jpeg'],
            ),
        ],
    )
    tags = models.ManyToManyField(Tag, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            generated_slug = f'{slugify(self.title)}-{uuid.uuid4()}'
            self.slug = generated_slug

        super().save(*args, **kwargs)

    @property
    def created_since(self):
        return get_time_since(self.created_at)

    # ----- COUNT -----
    @property
    def likes_count(self):
        return self.likes.count()

    @property
    def saves_count(self):
        return self.saves.count()

    # ----- URL -----
    def get_absolute_url(self):
        return reverse('photos:photo-detail', args=[self.slug])

    def get_delete_url(self):
        return reverse('photos:photo-delete', args=[self.slug])

    def get_like_url(self):
        return reverse('photos:photo-like', args=[self.slug])

    def get_unlike_url(self):
        return reverse('photos:photo-unlike', args=[self.slug])

    def get_save_url(self):
        return reverse('photos:photo-save', args=[self.slug])

    def get_unsave_url(self):
        return reverse('photos:photo-unsave', args=[self.slug])


class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='likes')
    photo = models.ForeignKey(Photo, on_delete=models.CASCADE, related_name='likes')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        unique_together = ['user', 'photo']

    def __str__(self):
        return f'{self.user.username} liked {self.photo.title}'


class Save(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='saves')
    photo = models.ForeignKey(Photo, on_delete=models.CASCADE, related_name='saves')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        unique_together = ['user', 'photo']

    def __str__(self):
        return f'{self.user.username} saved {self.photo.title}'
