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
    'ckeditor_uploader', # THÊM DÒNG NÀY ĐỂ KÍCH HOẠT UPLOADER
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
    # Tiêu đề hiển thị trên tab trình duyệt
    "site_title": "BJF Admin",

    # Tiêu đề ở góc trên bên trái
    "site_header": "BJF JEWELRY",

    # Logo cho trang admin
    "site_logo": None, # Bạn có thể trỏ tới file static logo, ví dụ: "images/logo.png"

    # Text chào mừng trên trang đăng nhập
    "welcome_sign": "Chào mừng đến với trang quản trị BJF",

    # Copyright ở footer
    "copyright": "BJF Jewelry Ltd",

    # Cấu hình menu sidebar
    "order_with_respect_to": [
        # --- NHÓM QUẢN LÝ NHÂN SỰ ---
        {
            "label": "Quản lý Nhân sự", 
            "icon": "fas fa-users-cog", 
            "models": [
                "store.NhanVien",
                "store.ChamCong",
                "store.PhongBan",
                "store.ChucVu",
            ]
        },

        # --- NHÓM QUẢN LÝ KINH DOANH ---
        {
            "label": "Quản lý Kinh doanh", 
            "icon": "fas fa-store-alt", 
            "models": [
                "store.Order",
                "store.Product",
                "store.Category",
                "store.Testimonial", # Nhận xét của khách hàng
                "store.ContactMessage",
            ]
        },

        # --- NHÓM NỘI DUNG & MARKETING ---
        {
            "label": "Nội dung & Marketing", 
            "icon": "fas fa-bullhorn",
            "models": [
                "store.Post",
                "store.Banner",
                "store.AboutPage",
            ]
        },

        # --- NHÓM TUYỂN DỤNG ---
        {
            "label": "Quản lý Tuyển dụng",
            "icon": "fas fa-briefcase",
            "models": [
                "store.JobPosting",
            ]
        },

        # --- NHÓM CÀI ĐẶT HỆ THỐNG ---
        {
            "label": "Hệ thống", 
            "icon": "fas fa-cogs", 
            "models": [
                "auth.User", # Quản lý tài khoản
                "auth.Group", # Quản lý nhóm quyền
                "store.SiteConfiguration",
                "store.ActionButton",
            ]
        },
    ],

    # Tùy chỉnh icon cho từng model cụ thể (tùy chọn)
    "icons": {
        "auth": "fas fa-users-cog",
        "auth.user": "fas fa-user",
        "auth.Group": "fas fa-users",
        "store.NhanVien": "fas fa-user-tie",
        "store.ChamCong": "fas fa-calendar-check",
        "store.PhongBan": "fas fa-building",
        "store.ChucVu": "fas fa-id-badge",
        "store.Order": "fas fa-file-invoice-dollar",
        "store.Product": "fas fa-gem",
        "store.Category": "fas fa-tags",
        "store.Post": "fas fa-newspaper",
        "store.Banner": "fas fa-image",
        "store.SiteConfiguration": "fas fa-cog",
        "store.JobPosting": "fas fa-briefcase",
        "store.Testimonial": "fas fa-comments",
        "store.ContactMessage": "fas fa-envelope",
        "store.AboutPage": "fas fa-info-circle",
        "store.ActionButton": "fas fa-mouse-pointer",
    },
}