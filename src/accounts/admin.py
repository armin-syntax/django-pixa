from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin

from .models import Relation


User = get_user_model()


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = (
        'username',
        'email',
        'full_name',
        'is_staff',
        'is_active',
        'created_at',
    )

    list_filter = (
        'is_staff',
        'is_superuser',
        'is_active',
        'groups',
    )

    search_fields = (
        'username',
        'email',
        'full_name',
        'bio',
    )

    ordering = ('-created_at',)

    readonly_fields = (
        'created_at',
        'updated_at',
        'last_login',
        'date_joined',
    )

    fieldsets = (
        (None, {
            'fields': (
                'username',
                'password',
            )
        }),
        ('Personal Information', {
            'fields': (
                'full_name',
                'email',
                'bio',
                'avatar',
            )
        }),
        ('Permissions', {
            'fields': (
                'is_active',
                'is_staff',
                'is_superuser',
                'groups',
                'user_permissions',
            )
        }),
        ('Important Dates', {
            'fields': (
                'last_login',
                'date_joined',
                'created_at',
                'updated_at',
            )
        }),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': (
                'username',
                'email',
                'full_name',
                'password1',
                'password2',
            ),
        }),
    )


@admin.register(Relation)
class RelationAdmin(admin.ModelAdmin):
    list_display = ('id', 'from_user', 'to_user', 'created_at')
    list_filter = ('from_user', 'to_user', 'created_at')
    search_fields = (
        'from_user__username',
        'from_user__email',
        'from_user__full_name',
        'from_user__bio',
        'to_user__username',
        'to_user__email',
        'to_user__full_name',
        'to_user__bio',
    )
