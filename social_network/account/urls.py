from django.urls import path
from . import views

app_name = 'account'
urlpatterns = [
    path('register/', views.RegisterView.as_view(), name='user_register'),
    path('login/', views.UserLoginView.as_view(), name='user_login'),
    path('logout/', views.UserLogoutView.as_view(), name='user_logout'),
    path('profile/<int:user_id>', views.UserProfileView.as_view(), name='user_profile'),
    path('reset/', views.UserPasswordResetView.as_view(), name='user_password_reset'),
    path('reset/done/', views.UserPasswordResetDoneView.as_view(), name='user_password_reset_done'),
    path('reset/complete/', views.UserPasswordResetCompleteView.as_view(), name='user_password_reset_complete'),
    path('confirm/<uidb64>/<token>/', views.UserPasswordResetConfirmView.as_view(), name='user_password_reset_confirm'),
    path('follow/<int:user_id>', views.UserFollowView.as_view(), name='user_follow'),
    path('unfollow/<int:user_id>', views.UserUnFollowView.as_view(), name='user_unfollow'),
    path('edit_user/', views.EditUserView.as_view(), name='user_edit'),
]
