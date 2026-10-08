import os
import sys
from dotenv import load_dotenv

import environ
from pathlib import Path
import mimetypes
mimetypes.add_type("video/mp4", ".mp4", True)

# Initialize django-environ
env = environ.Env(debug=(bool, False))

BASE_DIR = Path(__file__).resolve().parent.parent
environ.Env.read_env(BASE_DIR.parent / '.env')
load_dotenv(os.path.join(BASE_DIR, '.env'))

# 🔧 Add the 'src' folder to the Python path so Django can find the apps
sys.path.append(str(BASE_DIR / "src"))


# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = env('SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

# Dynamic
ALLOWED_HOSTS = ["www.jeremylebrun.dev",
                 "jeremylebrun.dev",
                 "83.228.243.130",
                 "localhost",
                 "127.0.0.1"]

CSRF_TRUSTED_ORIGINS = [
    "https://jeremylebrun.dev",
    "https://www.jeremylebrun.dev",
]

INSTALLED_APPS = [
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",

    # Your Django apps
    "users",
    "companies",
    "catalog",
    "inventory",
    "alerts",
    "dashboard",
    "core",
    "django_extensions",
    "portfolio",
    "captcha",

    # Your Wagtail apps
    "home",

    # Essential Wagtail apps
    "wagtail.contrib.forms",
    "wagtail.contrib.redirects",
    "wagtail.embeds",
    "wagtail.sites",
    "wagtail.users",
    "wagtail.snippets",
    "wagtail.documents",
    "wagtail.images",
    "wagtail.search",
    "wagtail.admin",
    "wagtail",
    "modelcluster",
    "taggit",
]



MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",   # <-- BEFORE Common & Csrf
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]


SESSION_ENGINE = "django.contrib.sessions.backends.signed_cookies"
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True


ROOT_URLCONF = 'config.urls'

LOGIN_URL = 'users:login'
# Redirect URL after a successful login
LOGIN_REDIRECT_URL = "/"  # or "/users/" depending on what you want
LOGOUT_REDIRECT_URL = "/users/login/"


TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS':[BASE_DIR / "templates"],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.messages.context_processors.messages',
                "core.context_processors.current_user",

            ],
        },
    },
]

WSGI_APPLICATION = 'config.wsgi.application'


# Choose the database depending on the environment
if os.getenv('DJANGO_ENV') == 'vps':
    DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.getenv('POSTGRES_DB', 'stock_manager_db'),
        'USER': os.getenv('POSTGRES_USER', 'postgres'),
        'PASSWORD': os.getenv('POSTGRES_PASSWORD', 'postgres'),
        'HOST': os.getenv('POSTGRES_HOST', 'localhost'),
        'PORT': os.getenv('POSTGRES_PORT', '5432'),
    }
}
else:
# local environment
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': os.getenv('POSTGRES_DB','stockdb'),
            'USER': os.getenv('POSTGRES_USER','postgres'),
            'PASSWORD': os.getenv('POSTGRES_PASSWORD','postgres'),
            'HOST': os.getenv('POSTGRES_HOST','localhost'),
            'PORT': os.getenv('POSTGRES_PORT','5432'),
        }
    }



AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.2/howto/static-files/

STATIC_URL = '/static/'
STATICFILES_DIRS = [BASE_DIR / 'static']  # for your global static files
STATIC_ROOT = BASE_DIR / 'staticfiles'   # destination

# MEDIA CONFIGURATION (For Wagtail: Images & Documents)

MEDIA_URL = "/media/"
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Sends emails via SMTP (production)
AUTH_USER_MODEL = "users.User"

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.infomaniak.com'
EMAIL_PORT = 465
EMAIL_USE_TLS = False  # Disable TLS
EMAIL_USE_SSL = True   # Enable SSL
EMAIL_HOST_USER = os.getenv('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = os.getenv('EMAIL_HOST_PASSWORD')
DEFAULT_FROM_EMAIL = os.getenv('DEFAULT_FROM_EMAIL')


# Site name for Wagtail admin
WAGTAIL_SITE_NAME = "My CMS"

# Base URL for Wagtail (used for notifications, user bar)
WAGTAILADMIN_BASE_URL = "https://www.jeremylebrun.dev/site/"

SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
USE_X_FORWARDED_HOST = True