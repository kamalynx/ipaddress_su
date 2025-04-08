from pathlib import Path

import environ

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


env = environ.Env(
    DEBUG=(bool, False),
)
env.read_env(".env")


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
# ~ SECRET_KEY = "django-insecure-a!l#%v-ng861f_g8sb!(4=0yd-f8jl)!o37a35%5*if=fm8a*+"
SECRET_KEY = env("SECRET_KEY")

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = env("DEBUG")

ALLOWED_HOSTS = env.tuple("ALLOWED_HOSTS")


# Application definition

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.contrib.sites",
    "django.contrib.sitemaps",
    "tinymce",
    "tools.apps.ToolsConfig",
    "articles.apps.ArticlesConfig",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "core.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        # ~ "DIRS": [
        # ~ BASE_DIR / 'templates',
        # ~ ],
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
    {
        "BACKEND": "django.template.backends.jinja2.Jinja2",
        "DIRS": [
            BASE_DIR / "templates",
        ],
        "APP_DIRS": True,
        "OPTIONS": {
            # ~ "match_extension": ".jinja",
            "environment": "core.jinja2.environment",
        },
    },
]

WSGI_APPLICATION = "core.wsgi.application"


# Database
# https://docs.djangoproject.com/en/5.1/ref/settings/#databases

DATABASES = {"default": env.db()}


# Password validation
# https://docs.djangoproject.com/en/5.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    # ~ {
    # ~ "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    # ~ },
    # ~ {
    # ~ "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    # ~ },
    # ~ {
    # ~ "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    # ~ },
    # ~ {
    # ~ "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    # ~ },
]


# Internationalization
# https://docs.djangoproject.com/en/5.1/topics/i18n/

LANGUAGE_CODE = "ru"

TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.1/howto/static-files/

MEDIA_URL = "media/"
STATIC_URL = "static/"
STATICFILES_DIRS = [BASE_DIR / "assets"]


if DEBUG:
    STATIC_ROOT = BASE_DIR / "static"
    MEDIA_ROOT = BASE_DIR / "media"
else:
    STATIC_ROOT = Path("/var/www/ipaddress.su/public/static")
    MEDIA_ROOT = Path("/var/www/ipaddress.su/public/media")

# Default primary key field type
# https://docs.djangoproject.com/en/5.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

SITE_ID = 1
