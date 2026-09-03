from django.urls import path

from . import views


app_name = 'accounts'
urlpatterns = [
    path('register/', views.UserRegisterView.as_view(), name='user-register'),
    path('login/', views.UserLoginView.as_view(), name='user-login'),
    path('logout/', views.UserLogoutView.as_view(), name='user-logout'),
    path('forgot-password/', views.UserForgotPasswordView.as_view(), name='user-forgot-password'),
    path('verify-code/', views.UserVerifyCodeView.as_view(), name='user-verify-code'),
    path('reset-password/', views.UserResetPasswordView.as_view(), name='user-reset-password'),
    path('<username>/', views.UserProfileView.as_view(), name='user-profile'),
    path('<username>/about/', views.UserProfileAboutView.as_view(), name='user-profile-about'),
    path('<username>/saved-photos/', views.UserSavedPhotosView.as_view(), name='user-saved-photos'),
    path('<username>/edit-profile/', views.UserEditProfileView.as_view(), name='user-edit-profile'),
    path('<username>/delete-account/', views.UserDeleteAccountView.as_view(), name='user-delete-account'),
    path('<username>/follow/', views.UserFollowView.as_view(), name='user-follow'),
    path('<username>/unfollow/', views.UserUnfollowView.as_view(), name='user-unfollow'),
]
