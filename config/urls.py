
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('super_cellar/', admin.site.urls),
    path('api/v1/', include('cella.urls')),
]
admin.site.site_header = "Cella Admin"
admin.site.site_title = "Cella Admin Portal"
admin.site.index_title = "Welcome To Cella Portal"