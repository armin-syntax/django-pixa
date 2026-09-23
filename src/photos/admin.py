from django.contrib import admin

from .models import Tag, Photo, Like, Save


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('name', 'slug')
    readonly_fields = ('slug', 'created_at')
    fields = ('name', 'slug', 'created_at')


@admin.register(Photo)
class PhotoAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'created_at')
    list_filter = ('created_at', 'user', 'tags')
    search_fields = ('title', 'caption', 'user__username', 'user__email')
    readonly_fields = ('created_at', 'updated_at')
    fields = ('user', 'title', 'caption', 'image', 'tags', 'created_at', 'updated_at')
    filter_horizontal = ('tags',)


@admin.register(Like)
class LikeAdmin(admin.ModelAdmin):
    list_display = ('user', 'photo', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('user__username', 'user__email', 'photo__title')
    readonly_fields = ('created_at',)
    fields = ('user', 'photo', 'created_at')


@admin.register(Save)
class SaveAdmin(admin.ModelAdmin):
    list_display = ('user', 'photo', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('user__username', 'user__email', 'photo__title')
    readonly_fields = ('created_at',)
    fields = ('user', 'photo', 'created_at')
