import os
import sys
from doctest import debug
from dotenv import load_dotenv


import environ
from pathlib import Path


# Initialise django-environ
env = environ.Env(debug=(bool, False))

# Build paths inside the project like this: BASE_DIR / 'subdir'.
#environ.Env.read_env(os.path.join(BASE_DIR, '.env'))
BASE_DIR = Path(__file__).resolve().parent.parent
environ.Env.read_env(BASE_DIR.parent / '.env')
load_dotenv(os.path.join(BASE_DIR, '.env'))

# 🔧 Ajout du dossier 'src' au path Python pour que Django trouve les apps
sys.path.append(str(BASE_DIR / "src"))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = env('SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False


#ALLOWED_HOSTS = ["127.0.0.1", "localhost", "testserver"]
#ALLOWED_HOSTS = ['localhost', '127.0.0.1', '.ngrok-free.app', '.ngrok-free.dev']

# Dynamic
ALLOWED_HOSTS = ["www.jeremylebrun.dev",
                 "jeremylebrun.dev",
                 "83.228.210.95",
                 "localhost",
                 "127.0.0.1"]
#NGROK_HOST = os.environ.get('NGROK_HOST')
#if NGROK_HOST:
    #ALLOWED_HOSTS.append(NGROK_HOST)

#CSRF_TRUSTED_ORIGINS = [
    #'https://*.ngrok-free.app',
   # 'https://*.ngrok-free.dev',
#]

INSTALLED_APPS = [
    #'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'users',
    'companies',
    'catalog',
    'inventory',
    'alerts',
    'dashboard',
    'core',
]


MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",   # <-- AVANT Common & Csrf
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
# URL de redirection après login réussi
LOGIN_REDIRECT_URL = "/"  # ou "/users/" selon ce que tu veux
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


# Database
# https://docs.djangoproject.com/en/5.2/ref/settings/#databases

# Choisir la base selon l'environnement
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
# environnement local
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



# Password validation
# https://docs.djangoproject.com/en/5.2/ref/settings/#auth-password-validators

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


# Internationalization
# https://docs.djangoproject.com/en/5.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.2/howto/static-files/

STATIC_URL = '/static/'
STATICFILES_DIRS = [BASE_DIR / 'static']  # pour ton static global
STATIC_ROOT = BASE_DIR / 'staticfiles'   # destination collectstatic


# Default primary key field type
# https://docs.djangoproject.com/en/5.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Envoie les mails dans la console (pour tester)
AUTH_USER_MODEL = "users.User"

EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend" # pour dev, écrit l'email dans le terminal
DEFAULT_FROM_EMAIL = 'webmaster@localhost'




