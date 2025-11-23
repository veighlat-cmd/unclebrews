"""
Django settings for myproject project.
Customized with Jazzmin for Uncle Brews Admin
"""

from pathlib import Path
import os
from decouple import config
import dj_database_url

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = config('SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = config('DEBUG', default=False, cast=bool)

ALLOWED_HOSTS = ['localhost', '127.0.0.1', '.onrender.com']


# Application definition
INSTALLED_APPS = [
    'jazzmin',  # 👈 Jazzmin must come before the default admin
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'myapp',  # your app
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'myproject.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'myproject.wsgi.application'


# Database
DATABASES = {
    'default': dj_database_url.config(
        default=config('DATABASE_URL', default='sqlite:///db.sqlite3'),
        conn_max_age=600,
        conn_health_checks=True,
    )
}


# Password validation
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]


# Internationalization
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'Asia/Manila'
USE_I18N = True
USE_TZ = True


# Static and Media files
STATIC_URL = '/static/'
STATICFILES_DIRS = [BASE_DIR / 'static']
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'


# Authentication Redirects
LOGIN_REDIRECT_URL = '/products/'
LOGOUT_REDIRECT_URL = '/'
LOGIN_URL = '/login/'


# Default primary key field type
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


# ----------------------------------------------------
# 🎨 JAZZMIN SETTINGS FOR UNCLE BREWS THEME
# ----------------------------------------------------
JAZZMIN_SETTINGS = {
    "site_title": "Uncle Brews Admin",
    "site_header": "Uncle Brews Dashboard",
    "site_brand": "Uncle Brews",
    "welcome_sign": "Welcome to Uncle Brews Admin Panel 🍵",
    "copyright": "Uncle Brews © 2025",
    "site_logo": "images/unclebrew.png",
    "login_logo": "images/unclebrew.png",
    "login_logo_dark": "images/unclebrew.png",
    "custom_css": "css/unclebrews.css",  # custom colors + background
    "show_ui_builder": True,

    # Top Menu
    "topmenu_links": [
        {"name": "Dashboard", "url": "admin:index", "permissions": ["auth.view_user"]},
        {"name": "Uncle Brews Website", "url": "/", "new_window": True},
    ],
    # --- Dashboard layout ---
    "related_modal_active": True,
    "show_ui_builder": False,

    # Icons
    "icons": {
        "auth": "fas fa-users-cog",
        "auth.user": "fas fa-user",
        "auth.Group": "fas fa-users",
        "myapp.Product": "fas fa-mug-hot",
    },

    # Sidebar
    "related_modal_active": True,
    "order_with_respect_to": ["auth", "myapp"],

    # UI Tweaks
    "navigation_expanded": True,
    "show_sidebar": True,
    "hide_apps": [],
    "hide_models": [],
}


# Optional UI Tweaks
JAZZMIN_UI_TWEAKS = {
    "theme": "sandstone",  # soft warm tone
    "dark_mode_theme": "solar",
    "navbar": "navbar-warning navbar-light",
    "no_navbar_border": True,
    "body_small_text": False,
    "brand_colour": "navbar-warning",
    "accent": "accent-warning",
    "sidebar": "sidebar-light-warning",
    "sidebar_nav_small_text": False,
    "sidebar_disable_expand": False,
    "sidebar_nav_flat_style": False,
    "sidebar_nav_child_indent": True,
    "sidebar_nav_compact_style": False,
    "button_classes": {
        "primary": "btn-warning",
        "secondary": "btn-outline-warning",
    },
}
