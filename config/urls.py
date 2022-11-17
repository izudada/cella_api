
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('super_cellar/', admin.site.urls),
    path('api/v1/', include('cella.urls')),
    path('api/v1/auth/password_reset', include('django_rest_passwordreset.urls', namespace='password_reset')),

]
admin.site.site_header = "Cella Admin"
admin.site.site_title = "Cella Admin Portal"
admin.site.index_title = "Welcome To Cella Portal"