import os
import sys
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = os.getenv("SECRET_KEY", "django-insecure-g9fii$$")

DEBUG = True

ALLOWED_HOSTS = []

INSTALLED_APPS = [
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "WGForge.cats",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "WGForge.middleware.CatLimitViewMiddleware",
]

ROOT_URLCONF = "WGForge.urls"

WSGI_APPLICATION = "WGForge.wsgi.application"

is_test = "manage.py" in sys.argv and "test" in sys.argv

if is_test:
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": os.path.join(BASE_DIR, "db.sqlite3"),
        }
    }
else:
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.postgresql",
            "NAME": os.getenv("POSTGRES_DB", "wg_forge_db"),
            "USER": os.getenv("POSTGRES_USER", "wg_forge"),
            "PASSWORD": os.getenv("POSTGRES_PASSWORD", "42a"),
            "HOST": os.getenv("POSTGRES_HOST", "localhost"),
            "PORT": os.getenv("POSTGRES_PORT", "5432"),
        }
    }

LANGUAGE_CODE = "en-us"
TIME_ZONE = "Europe/Moscow"
USE_TZ = True

CAT_VIEW_LIMIT = {
    "PATH": "/cats",
    "METHOD": "GET",
    "LIMIT": "600/m",
    "CACHE_NAME": "cat_view_limit",
}
