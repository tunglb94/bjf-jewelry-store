# bjf_project/bjf_project/settings.py

import os
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = 'django-insecure-a#y(w2-!9z@$p!#^n&!_y_q*!@s#d$f%g&h*j(k)l'

# Tắt DEBUG khi chạy trên server
DEBUG = False

# Thêm tên miền của bạn vào đây
ALLOWED_HOSTS = ['tunglb941.pythonanywhere.com']


# Application definition
INSTALLED_APPS = [
    'jazzmin',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.humanize',
    'solo',
    'store.apps.StoreConfig',
    'ckeditor',
    'ckeditor_uploader',
    'django_group_by',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'bjf_project.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'store.context_processors.site_settings',
            ],
        },
    },
]

WSGI_APPLICATION = 'bjf_project.wsgi.application'

# Database
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# Password validation
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# Internationalization
LANGUAGE_CODE = 'vi'
TIME_ZONE = 'Asia/Ho_Chi_Minh'
USE_I18N = True
USE_TZ = True

# Static & Media files
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

# Đường dẫn chính xác để Django tìm thấy thư mục static chứa logo và CSS
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'bjf_project', 'static'),
]

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# Default primary key field type
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# === CẤU HÌNH CKEDITOR CHUYÊN NGHIỆP ===
CKEDITOR_UPLOAD_PATH = "uploads/"
CKEDITOR_CONFIGS = {
    'default': {
        'toolbar': 'full',
        'height': 300,
        'width': '100%',
        'extraPlugins': ','.join([
            'uploadimage', 'div', 'autolink', 'autoembed', 'embedsemantic',
            'autogrow', 'widget', 'lineutils', 'clipboard', 'dialog',
            'dialogui', 'elementspath'
        ]),
    },
}

# =======================================================
# ==            CẤU HÌNH GIAO DIỆN JAZZMIN             ==
# =======================================================

JAZZMIN_SETTINGS = {
    "site_title": "BJF Admin",
    "site_header": "BJF GROUP",
    "site_brand": "TẬP ĐOÀN BJF GROUP",
    
    "site_logo": "img/logo_bjf_group.png",
    "login_logo": "img/logo_bjf_group.png",
    
    "welcome_sign": "Chào mừng đến với trang quản trị Tập đoàn BJF Group",
    "copyright": "BJF Group Ltd",
    
    # THÊM DÒNG NÀY ĐỂ NHẬN FILE CSS TÙY CHỈNH
    "custom_css": "css/custom_jazzmin.css",

    "order_with_respect_to": [
        "store.NhanVien", "store.ChamCong", "store.PhongBan", "store.ChucVu",
        "store.BatDongSan",
        "store.Order", "store.Product", "store.Category",
        "store.Post", "store.Banner",
        "auth.User", "auth.Group",
        "store.SiteConfiguration",
    ],

    "icons": {
        "auth.user": "fas fa-user",
        "auth.Group": "fas fa-users",
        "store.NhanVien": "fas fa-user-tie",
        "store.ChamCong": "fas fa-calendar-check",
        "store.PhongBan": "fas fa-building",
        "store.ChucVu": "fas fa-id-badge",
        "store.BatDongSan": "fas fa-city",
        "store.Order": "fas fa-file-invoice-dollar",
        "store.Product": "fas fa-gem",
        "store.Category": "fas fa-tags",
        "store.Post": "fas fa-newspaper",
        "store.Banner": "fas fa-image",
        "store.SiteConfiguration": "fas fa-cog",
    },
}