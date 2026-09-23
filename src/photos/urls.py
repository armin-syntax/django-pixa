from django.urls import path

from . import views


app_name = 'photos'
urlpatterns = [
    path('', views.PhotosView.as_view(), name='photos'),
    path('tags/', views.TagsView.as_view(), name='tags'),
    path('upload/', views.PhotoUploadView.as_view(), name='photo-upload'),
    path('<public_id>/', views.PhotoDetailView.as_view(), name='photo-detail'),
    path('<public_id>/update/', views.PhotoUpdateView.as_view(), name='photo-update'),
    path('<public_id>/delete/', views.PhotoDeleteView.as_view(), name='photo-delete'),
    path('<public_id>/like/', views.PhotoLikeView.as_view(), name='photo-like'),
    path('<public_id>/unlike/', views.PhotoUnlikeView.as_view(), name='photo-unlike'),
    path('<public_id>/save/', views.PhotoSaveView.as_view(), name='photo-save'),
    path('<public_id>/unsave/', views.PhotoUnsaveView.as_view(), name='photo-unsave'),
]
