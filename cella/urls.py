from django.urls import  include, path
from . import views


urlpatterns = [
    #Auth
    path('auth/verify', views.verify_user),
    path('auth/hello', views.say_hello, name="test"),
    path('auth/checkout', views.checkout, name="checkout"),
    path('auth/login', views.login_user, name="login"),

    #   Brands
    path('brands/all', views.BrandApiListView.as_view(), name="brands"),
    path('brands', views.brand_create_view, name="brands"),
    path('brands/edit', views.brand_update_view, name="edit_brand"),
    path('brands/delete', views.brand_delete_view, name="delete_brand"),

    #Products
    path('products/all', views.ProductApiListView.as_view(), name="products"),
    path('products', views.product_create_view, name="create_product"),
    path('products/edit', views.product_update_view, name="edit_product"),
    path('products/delete', views.product_delete_view, name="delete_product"),
    path('product/<str:uuid>', views.product_detail_view, name="product"),
]