from django import forms
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
                allowed_extensions=['png', 'jpg', 'jpeg', 'webp'],
            ),
        ],
        widget=forms.FileInput(attrs={
            'id': 'photo',
            'accept': 'image/jpeg,image/png,image/webp',
        }),
    )
    tags = forms.CharField(
        required=False,
        widget=forms.HiddenInput(),
    )

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
        
        tag_list = [tag.strip().lower() for tag in tags.split(',') if tag.strip()]
        
        if len(tag_list) > 8:
            raise forms.ValidationError('Maximum 8 tags allowed.')
        
        valid_tags = set(Tag.objects.values_list('name', flat=True))
        valid_tags_lower = {tag.lower() for tag in valid_tags}
        
        for tag in tag_list:
            if tag not in valid_tags_lower:
                raise forms.ValidationError(f'Tag "{tag}" is not available.')
        
        return tag_list
    
    def save(self, user):
        cd = self.cleaned_data
        
        photo = Photo.objects.create(
            user=user,
            title=cd['title'],
            caption=cd.get('caption', ''),
            image=cd['image'],
        )
        
        for tag_name in cd.get('tags', []):
            tag = Tag.objects.get(name__iexact=tag_name)
            photo.tags.add(tag)
        
        return photo
