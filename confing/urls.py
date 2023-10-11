from django.contrib import admin
from django.urls import path, include
from video_site import views as video_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('video/', include('video_site.urls')),
]
