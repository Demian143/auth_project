from django.urls import path
from . import views

app_name = 'authentication'
urlpatterns = [
    path('signin/', views.SignInView.as_view(), name='signin'),
    path('login/', views.LoginView.as_view(), name='user_login'),
    path('logout/', views.user_logout, name='user_logout'),
    path('user_home/', views.user_home_page, name='user_home'),
    path('update_password/', views.update_password, name='update_password'),
    path('update_username/', views.update_username, name='update_username'),
    path('update_email/', views.update_email, name='update_email'),
    path('delete_account', views.delete_account, name='delete_account'),
]
