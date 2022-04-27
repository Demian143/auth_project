from django.urls import path
from . import views

app_name = 'authentication'
urlpatterns = [
    path('signin/', views.SignInView.as_view(), name='signin'),
    path('login/', views.LoginView.as_view(), name='user_login'),
    path('logout/', views.user_logout, name='user_logout'),
    path('user_home/', views.UserHomeView.as_view(), name='user_home'),
    path('update_password/', views.UpdatePasswordView.as_view(),
         name='update_password'),
    path('update_username/', views.UpdateUserNameView.as_view(),
         name='update_username'),
    path('delete_account', views.DeleteAccountView.as_view(), name='delete_account'),
    path('update_email/', views.update_email, name='update_email'),
]
