import os
import uuid

from django.conf import settings


def user_avatar_upload_path(instance, filename):
    extension = os.path.splitext(filename)[1].lower()
    file_name = f'avatar{extension}'
    file_path = f'accounts/{instance.pk}/{file_name}'
    full_path = os.path.join(settings.MEDIA_ROOT, file_path)

    if os.path.isfile(full_path):
        os.remove(full_path)

    return file_path


def photo_upload_path(instance, filename):
    extension = os.path.splitext(filename)[1].lower()
    file_name = f'{uuid.uuid4()}{extension}'

    return f'accounts/{instance.user.pk}/photos/{file_name}'
