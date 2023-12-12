from django.contrib import admin
from django.urls import path, include
from django.urls import re_path


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('webflut.urls')),
    re_path('', include('pwa.urls')),  # You MUST use an empty string as the URL prefix
]
