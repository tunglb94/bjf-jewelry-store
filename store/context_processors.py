# bjf_project/store/context_processors.py

from .models import SiteConfiguration, ActionButton

def site_settings(request):
    try:
        settings = SiteConfiguration.objects.get()
    except SiteConfiguration.DoesNotExist:
        settings = {}
    
    # Lấy tất cả các nút hành động đang được kích hoạt
    action_buttons = ActionButton.objects.filter(is_active=True)
        
    return {
        'settings': settings,
        'action_buttons': action_buttons,
    }