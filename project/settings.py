"""
Django settings for project project.
"""
import os
from pathlib import Path
import dj_database_url

BASE_DIR = Path(__file__).resolve().parent.parent

# SECURITY WARNING: en producción esta clave debe venir de una variable de entorno.
SECRET_KEY = os.getenv("DJANGO_SECRET_KEY", "664za+^rz^pv5wqrz44p0yg!@$%vf(jo)ml4t%!wd9d7zlgjm!")

DEBUG = os.getenv("DJANGO_DEBUG", "1") == "1"

ALLOWED_HOSTS = ["inesplaza.azurewebsites.net", "localhost", "127.0.0.1"]

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'crispy_forms',
    'relecloud.apps.RelecloudConfig',
    'crispy_bootstrap4',
]

CRISPY_ALLOWED_TEMPLATE_PACKS = ("bootstrap4",)
CRISPY_TEMPLATE_PACK = "bootstrap4"

CSRF_TRUSTED_ORIGINS = [
    'https://inesplaza.azurewebsites.net',
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

ROOT_URLCONF = 'project.urls'

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

WSGI_APPLICATION = 'project.wsgi.application'

# Database
# Si existe DATABASE_URL se usa esa (p.ej. sqlite en tests / CI).
# Si no, se usan las variables de entorno de PostgreSQL (Azure).
DATABASE_URL = os.getenv("DATABASE_URL")
if DATABASE_URL:
    DATABASES = {
        "default": dj_database_url.parse(DATABASE_URL, conn_max_age=600)
    }
else:
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.postgresql",
            "NAME": os.getenv("DJANGO_DB_NAME", "inesbbdd"),
            "USER": os.getenv("DJANGO_DB_USER", "ines"),
            "PASSWORD": os.getenv("DJANGO_DB_PASSWORD", "29112003i_"),
            "HOST": os.getenv("DJANGO_DB_HOST", "inesserver.postgres.database.azure.com"),
            "PORT": os.getenv("DJANGO_DB_PORT", "5432"),
            "OPTIONS": {"sslmode": os.getenv("DJANGO_DB_SSLMODE", "require")},
        }
    }

AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_L10N = True
USE_TZ = True

STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / "staticfiles"

# --- PT1: configuración de correo ---
# Por defecto (desarrollo) imprime el correo en consola.
EMAIL_BACKEND = os.getenv(
    "DJANGO_EMAIL_BACKEND",
    "django.core.mail.backends.console.EmailBackend",
)
EMAIL_HOST = os.getenv("EMAIL_HOST", "smtp.gmail.com")
EMAIL_PORT = int(os.getenv("EMAIL_PORT", "587"))
EMAIL_USE_TLS = os.getenv("EMAIL_USE_TLS", "1") == "1"
EMAIL_HOST_USER = os.getenv("EMAIL_HOST_USER", "")
EMAIL_HOST_PASSWORD = os.getenv("EMAIL_HOST_PASSWORD", "")
DEFAULT_FROM_EMAIL = os.getenv("DEFAULT_FROM_EMAIL", "noreply@relecloud.com")
INFO_REQUEST_RECIPIENT = os.getenv("INFO_REQUEST_RECIPIENT", "ventas@relecloud.com")
