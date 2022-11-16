from django.urls import  include, path
from . import views


urlpatterns = [
    path('auth/verify', views.verify_user),
    path('auth/hello', views.say_hello, name="test"),
    path('auth/checkout', views.checkout, name="checkout"),
    path('auth/login', views.login_user, name="login"),


    path('brands/all', views.BrandApiListView.as_view(), name="brands"),
    path('brands', views.brand_create_view, name="brands"),
    path('products', views.ProductApiListView.as_view(), name="products"),
]