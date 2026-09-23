from django import forms
from django.db import transaction
from django.core.validators import FileExtensionValidator

from .models import Tag, Photo


class PhotoUploadForm(forms.Form):
    title = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={
            'id': 'title',
            'class': 'field',
            'placeholder': 'Give your photo a title',
            'maxlength': '100',
        }),
        error_messages={
            'required': 'Title is required.',
        },
    )

    caption = forms.CharField(
        max_length=200,
        required=False,
        widget=forms.Textarea(attrs={
            'id': 'caption',
            'class': 'field',
            'placeholder': 'Write a short caption...',
            'maxlength': '200',
            'rows': '3',
        }),
    )
    image = forms.ImageField(
        required=True,
        validators=[
            FileExtensionValidator(
                allowed_extensions=['png', 'jpg', 'jpeg'],
            ),
        ],
        widget=forms.FileInput(attrs={
            'id': 'photo',
            'accept': 'image/jpeg,image/png,image/webp',
        }),
    )
    tags = forms.CharField(required=False, widget=forms.HiddenInput())

    def clean_image(self):
        image = self.cleaned_data.get('image')

        if not image:
            raise forms.ValidationError('Please select a photo.')

        if image.size > 5 * 1024 * 1024:
            raise forms.ValidationError('File size must be less than 5MB.')

        if not image.content_type.startswith('image/'):
            raise forms.ValidationError('File must be an image.')

        return image

    def clean_tags(self):
        tags = self.cleaned_data.get('tags', '')

        if not tags:
            return []

        tag_list = [
            tag.strip().lower()
            for tag in tags.split(',')
            if tag.strip()
        ]

        tag_list = list(dict.fromkeys(tag_list))

        if len(tag_list) > 8:
            raise forms.ValidationError('Maximum 8 tags allowed.')

        valid_tags = Tag.objects.values_list('name', flat=True)

        valid_tags_lower = {
            tag.lower()
            for tag in valid_tags
        }

        for tag in tag_list:
            if tag not in valid_tags_lower:
                raise forms.ValidationError(f'Tag "{tag}" is not available.')

        return tag_list

    @transaction.atomic
    def save(self, user):
        cd = self.cleaned_data

        photo = Photo.objects.create(
            user=user,
            title=cd['title'],
            caption=cd['caption'],
            image=cd['image'],
        )

        tag_objects = []

        for tag_name in cd['tags']:
            tag = Tag.objects.filter(name__iexact=tag_name).first()

            if tag:
                tag_objects.append(tag)

        photo.tags.set(tag_objects)

        return photo


class PhotoUpdateForm(forms.Form):
    title = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={
            'id': 'title',
            'class': 'field',
            'placeholder': 'Give your photo a title',
            'maxlength': '100',
        }),
        error_messages={
            'required': 'Title is required.',
        },
    )

    caption = forms.CharField(
        max_length=200,
        required=False,
        widget=forms.Textarea(attrs={
            'id': 'caption',
            'class': 'field',
            'placeholder': 'Write a short caption...',
            'maxlength': '200',
            'rows': '3',
        }),
    )

    tags = forms.CharField(
        required=False,
        widget=forms.HiddenInput(),
    )

    def __init__(self, *args, **kwargs):
        self.photo = kwargs.pop('photo', None)
        super().__init__(*args, **kwargs)

    def clean_tags(self):
        tags = self.cleaned_data.get('tags', '')

        if not tags:
            return []

        tag_list = [
            tag.strip()
            for tag in tags.split(',')
            if tag.strip()
        ]

        tag_list = list(dict.fromkeys(
            tag.lower()
            for tag in tag_list
        ))

        if len(tag_list) > 8:
            raise forms.ValidationError('Maximum 8 tags allowed.')

        valid_tags = Tag.objects.values_list('name', flat=True)

        valid_tags_lower = {
            tag.lower()
            for tag in valid_tags
        }

        for tag in tag_list:
            if tag not in valid_tags_lower:
                raise forms.ValidationError(f'Tag "{tag}" is not available.')

        return tag_list

    @transaction.atomic
    def save(self):
        if self.photo is None:
            raise ValueError('PhotoUpdateForm requires a photo instance.')

        self.photo.title = self.cleaned_data['title']
        self.photo.caption = self.cleaned_data['caption']
        self.photo.save()

        tag_objects = []

        for tag_name in self.cleaned_data['tags']:
            tag = Tag.objects.filter(name__iexact=tag_name).first()

            if tag:
                tag_objects.append(tag)
        
        self.photo.tags.set(tag_objects)

        return self.photo
