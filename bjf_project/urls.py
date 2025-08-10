# bjf_project/bjf_project/urls.py

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    # Dòng này đã được sửa lại để không còn namespace
    # Đảm bảo file của bạn sử dụng dòng này, không có "namespace='store'"
    path('', include('store.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
