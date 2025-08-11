# bjf_project/bjf_project/urls.py

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    # THÊM DÒNG NÀY ĐỂ KÍCH HOẠT CHỨC NĂNG UPLOAD ẢNH
    path('ckeditor/', include('ckeditor_uploader.urls')),
    path('', include('store.urls')),
]

# Dòng này chỉ dùng khi DEBUG=True, trên production PythonAnywhere không dùng
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)