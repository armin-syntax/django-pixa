from django.urls import path
from django.contrib.auth import views as auth_views

from . import views


app_name = 'accounts'
urlpatterns = [
    path('register/', views.UserRegisterView.as_view(), name='user-register'),
    path('login/', views.UserLoginView.as_view(), name='user-login'),
    path('logout/', views.UserLogoutView.as_view(), name='user-logout'),

    # ----------------------------------------------------
    # Password Reset (with Django Auth Views)

    path('forgot-password/', 
         auth_views.PasswordResetView.as_view(
             template_name='accounts/forgot_password.html',
             email_template_name='accounts/password_reset_email.html',
             subject_template_name='accounts/password_reset_subject.txt',
             success_url='/accounts/reset-password-done/'
         ),
         name='user-forgot-password'),
    
    path('reset-password-done/',
         auth_views.PasswordResetDoneView.as_view(
             template_name='accounts/reset_password_done.html'
         ),
         name='user-reset-password-done'),
    
    path('reset-password-confirm/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(
             template_name='accounts/reset_password_confirm.html',
             success_url='/accounts/reset-password-complete/'
         ),
         name='user-reset-password-confirm'),
    
    path('reset-password-complete/',
         auth_views.PasswordResetCompleteView.as_view(
             template_name='accounts/reset_password_complete.html'
         ),
         name='user-reset-password-complete'),

    # ----------------------------------------------------

    path('<username>/', views.UserProfileView.as_view(), name='user-profile'),
    path('<username>/about/', views.UserProfileAboutView.as_view(), name='user-profile-about'),
    path('<username>/saved-photos/', views.UserSavedPhotosView.as_view(), name='user-saved-photos'),
    path('<username>/edit-profile/', views.UserEditProfileView.as_view(), name='user-edit-profile'),
    path('<username>/delete-avatar/', views.UserDeleteAvatarView.as_view(), name='user-delete-avatar'),
    path('<username>/delete-account/', views.UserDeleteAccountView.as_view(), name='user-delete-account'),
    path('<username>/follow/', views.UserFollowView.as_view(), name='user-follow'),
    path('<username>/unfollow/', views.UserUnfollowView.as_view(), name='user-unfollow'),
]
