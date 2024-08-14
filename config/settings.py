import os
from pathlib import Path

from dotenv import load_dotenv


# Getting the base project directory
BASE_DIR = Path(__file__).resolve().parent.parent


if os.getenv("ENVIRONMENT") == "docker":
    env_file = ".env.docker"
else:
    env_file = ".env.local"
dotenv_path = BASE_DIR / env_file

if dotenv_path.exists():
    load_dotenv(dotenv_path)


# Settings Django project
SECRET_KEY = os.environ.get("SECRET_KEY", "django-bad-secret-key")
DEBUG = os.environ.get("DEBUG", "False") == "True"


# Application definition
INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    # My apps
    "apps.diary",
    "apps.users",
]

# Settings middleware
MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

# Settings urls
ALLOWED_HOSTS = ["*"]
ROOT_URLCONF = "config.urls"


TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]


WSGI_APPLICATION = "config.wsgi.application"


# Settings Database
DATABASES = {
    "default": {
        # "ENGINE": f"django.db.backends.{os.environ.get('POSTGRES_ENGINE', 'postgresql_psycopg2')}",
        "ENGINE": "django.db.backends.postgresql_psycopg2",
        "NAME": os.environ.get("POSTGRES_DB", "personal_diary"),
        "USER": os.environ.get("POSTGRES_USER", "postgres"),
        "PASSWORD": os.environ.get("POSTGRES_PASSWORD", "SecretPassword"),
        "HOST": os.environ.get("POSTGRES_HOST", "localhost"),
        "PORT": os.environ.get("POSTGRES_PORT", 5432),
    }
}


# Password validation
AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]


# Internationalization
LANGUAGE_CODE = "ru"
TIME_ZONE = "UTC"
USE_I18N = True
USE_TZ = True


# Settings static files (CSS, JavaScript, Images) and media files
STATIC_URL = "/static/"
STATIC_ROOT = os.path.join(BASE_DIR, "static")

MEDIA_URL = "/media/"
MEDIA_ROOT = os.path.join(BASE_DIR, "media")


# Default primary key field type
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"


# Settings Users
AUTH_USER_MODEL = "users.Users"


# Settings host-email
EMAIL_BACKEND = os.environ.get("EMAIL_BACKEND", "django.core.mail.backends.smtp.EmailBackend")
EMAIL_HOST = os.environ.get("EMAIL_HOST", "smtp.yandex.ru")
EMAIL_PORT = os.environ.get("EMAIL_PORT", 465)
EMAIL_USE_SSL = True
EMAIL_USE_TLS = False

EMAIL_HOST_USER = os.environ.get("EMAIL_HOST_USER", "my_email@yandex.ru")
EMAIL_HOST_PASSWORD = os.environ.get("EMAIL_HOST_PASSWORD", "SecretPassword")
DEFAULT_FROM_EMAIL = EMAIL_HOST_USER


# Login / Logout / Registry
LOGIN_REDIRECT_URL = "/diary"
LOGOUT_REDIRECT_URL = "/"
