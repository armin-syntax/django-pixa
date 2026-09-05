from django.urls import path

from . import views


app_name = 'photos'
urlpatterns = [
    path('', views.PhotosView.as_view(), name='photos'),
    path('tags/', views.TagListView.as_view(), name='tags'),
    path('upload/', views.PhotoUploadView.as_view(), name='photo-upload'),
    path('<slug:slug>/', views.PhotoDetailView.as_view(), name='photo-detail'),
    path('<slug:slug>/delete/', views.PhotoDeleteView.as_view(), name='photo-delete'),
    path('<slug:slug>/like/', views.PhotoLikeView.as_view(), name='photo-like'),
    path('<slug:slug>/unlike/', views.PhotoUnlikeView.as_view(), name='photo-unlike'),
    path('<slug:slug>/save/', views.PhotoSaveView.as_view(), name='photo-save'),
    path('<slug:slug>/unsave/', views.PhotoUnsaveView.as_view(), name='photo-unsave'),
]
