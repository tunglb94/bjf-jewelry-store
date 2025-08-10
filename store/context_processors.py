# bjf_project/store/context_processors.py

from .models import SiteConfiguration

def site_settings(request):
    try:
        settings = SiteConfiguration.objects.get()
    except SiteConfiguration.DoesNotExist:
        # Nếu chưa có đối tượng cài đặt, trả về một dictionary rỗng
        # để website không bị lỗi.
        settings = {}
        
    return {
        'settings': settings
    }
