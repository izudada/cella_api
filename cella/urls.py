from django.urls import  include, path
from . import views


urlpatterns = [
    path('auth/verify', views.verify_user),
    path('auth/hello', views.say_hello, name="test"),
    path('auth/checkout', views.checkout, name="checkout"),
    path('auth/login', views.login_user, name="login"),


    path('brands/all', views.BrandApiListView.as_view(), name="brands"),
    path('brands', views.brand_create_view, name="brands"),
    path('brands/edit', views.brand_update_view, name="edit_brand"),
    path('brands/delete', views.brand_delete_view, name="delete_brand"),
    path('products/all', views.ProductApiListView.as_view(), name="products"),
]