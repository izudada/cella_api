from django.urls import  include, path
from . import views


urlpatterns = [
    #Auth
    path('auth/verify', views.verify_user),
    path('auth/hello', views.say_hello, name="test"),
    path('auth/checkout', views.checkout, name="checkout"),
    path('auth/login', views.login_user, name="login"),


    #   Password change
    path('auth/change-password', views.ChangePasswordView.as_view(), name='change-password'),
    path('auth/password_reset', include('django_rest_passwordreset.urls', namespace='password_reset')),

    #   Brands
    path('brands/all', views.BrandApiListView.as_view(), name="brands"),
    path('brands', views.brand_create_view, name="brands"),
    path('brands/edit', views.brand_update_view, name="edit_brand"),
    path('brands/delete', views.brand_delete_view, name="delete_brand"),
    path('brands/<str:uuid>', views.brand_detail_view, name="view_brand"),

    #Products
    path('products/all', views.ProductApiListView.as_view(), name="products"),
    path('products', views.product_create_view, name="create_product"),
    path('products/edit', views.product_update_view, name="edit_product"),
    path('products/delete', views.product_delete_view, name="delete_product"),
    path('products/<str:uuid>', views.product_detail_view, name="product"),

    path('orders/<str:ref>', views.order_detail_view, name="view_order"),

]
