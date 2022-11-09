from django.urls import  include, path
from . import views


urlpatterns = [
    path('auth/users', views.RegisterAPI.as_view(), name="register"),
    path('auth/verify', views.verify_user),
    path('auth/login', views.login_user, name="login"),
]