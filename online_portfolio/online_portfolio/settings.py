"""
Django settings for online_portfolio project.

Generated by 'django-admin startproject' using Django 3.0.7.

For more information on this file, see
https://docs.djangoproject.com/en/3.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.0/ref/settings/
"""

from decouple import config
import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = config("SECURITY_KEY")

ENV = config("ENV", default="local")
# SECURITY WARNING: don't run with debug turned on in production!

if ENV == "local":
    DEBUG = True
    ALLOWED_HOSTS = []

elif ENV == "prod":
    DEBUG = False
    ALLOWED_HOSTS = ["www.online-portfolio.live"]

ADMINS = [
    ("manthan", "manthanchauhan913@gmail.com"),
]
# Application definition

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "accounts",
    "portfolio",
    "storages",
    "phonenumber_field",
    "social_django",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "social_django.middleware.SocialAuthExceptionMiddleware",
]

AUTHENTICATION_BACKENDS = (
    "social_core.backends.github.GithubOAuth2",
    "django.contrib.auth.backends.ModelBackend",
)

ROOT_URLCONF = "online_portfolio.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [os.path.join(BASE_DIR, "templates"),],
        "APP_DIRS": False,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                "social_django.context_processors.backends",
                "social_django.context_processors.login_redirect",
            ],
        },
    },
]

WSGI_APPLICATION = "online_portfolio.wsgi.application"


# Database
# https://docs.djangoproject.com/en/3.0/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql_psycopg2",
        "NAME": "portfolio",
        "USER": "portfolio",
        "PASSWORD": config("DB_PASSWORD"),
        "HOST": "localhost",
        "PORT": "",
    }
}

# Password validation
# https://docs.djangoproject.com/en/3.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",},
]


# Internationalization
# https://docs.djangoproject.com/en/3.0/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Email settings
EMAIL_HOST = "smtp.gmail.com"
EMAIL_HOST_USER = "pythonic913@gmail.com"
DEFAULT_FROM_EMAIL = EMAIL_HOST_USER
EMAIL_HOST_PASSWORD = config("EMAIL_PASSWORD")
EMAIL_PORT = 587
EMAIL_USE_TLS = True

# Login settings
LOGIN_REDIRECT_URL = "/portfolio/edit/"
LOGIN_URL = "/accounts/login/"
LOGOUT_URL = "/accounts/logout/"
LOGOUT_REDIRECT_URL = "/accounts/login/"

# static files (Amazon S3) configuration
AWS_ACCESS_KEY_ID = config("AWS_ACCESS_KEY")
AWS_SECRET_ACCESS_KEY = config("AWS_SECRET_ACCESS_KEY")
AWS_STORAGE_BUCKET_NAME = "online-portfolio123"
AWS_DEFAULT_ACL = None
AWS_S3_CUSTOM_DOMAIN = AWS_STORAGE_BUCKET_NAME + ".s3.amazonaws.com"

AWS_S3_OBJECT_PARAMETERS = {
    "CacheControl": "max-age=86400",
}

AWS_LOCATION = "static"

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.0/howto/static-files/

STATICFILES_DIRS = [
    os.path.join(BASE_DIR, "static"),
]

if ENV == "prod":
    STATIC_URL = "https://" + AWS_S3_CUSTOM_DOMAIN + "/" + AWS_LOCATION + "/"
    STATICFILES_STORAGE = "storages.backends.s3boto3.S3Boto3Storage"

else:
    STATIC_URL = "/static/"


# phone number setup
PHONENUMBER_DB_FORMAT = "INTERNATIONAL"

# user uploaded files
MEDIA_ROOT = os.path.join(BASE_DIR, "media")
MEDIA_URL = "/media/"
DEFAULT_FILE_STORAGE = "online_portfolio.classes.MediaStorage"

# OAuth settings
SOCIAL_AUTH_GITHUB_KEY = config("GITHUB_KEY")
SOCIAL_AUTH_GITHUB_SECRET = config("GITHUB_SECRET")

# app functionality settings
DEFAULT_BASIC_INFO = {
    "name": "Manthan Chauhan",
    "about": '<div style=""><span style="font-size: 24px; background-color: rgb(255, 198, 156);">I\'m a <u style="">Backend Engineer</u><b style="">&nbsp;</b>whose top priorities are <b style="">Speed</b>, <b style="">Scalability</b>, <b style="">Security </b>&amp; <b style="">Reliability</b>.</span></div><div style=""><span style="font-size: 24px;"><br></span></div><p><span style="font-size: 24px;">I also have knowledge of basic Frontend technologies and I\'m capable of building <b>Complex Systems </b>entirely <u>from scratch</u>.</span></p><div style=""><span style="font-size: 24px;"><br></span></div><div style=""><span style="font-size: 24px;">I\'ve <b>leaded </b>software development teams towards the&nbsp;<b>GOAL </b>multiple times. I\'m a <u>team leader</u>&nbsp;&amp;&nbsp;<u>team builder</u>.</span></div>',
    "tag_line": "Django Developer & Competitive Programmer",
    "profile_pic": "https://online-portfolio123.s3.ap-south-1.amazonaws.com/static/portfolio/avatar.png",
}

DEFAULT_PROJECT = {
    "title": "Project Title",
    "description": "Project Description",
    "skills": "Skills Utilized",
    "image": "https://online-portfolio123.s3.ap-south-1.amazonaws.com/static/portfolio/763856+(1).jpg",
}
DEFAULT_USER = "manthanchauhan913@gmail.com"

DEFAULT_SKILLS = {
    "Programming Languages": ["C", "C++", "Python", "Embedded C"],
    "Web Development": [
        "Django",
        "Django Rest Framework",
        "PostgreSQL",
        "Apache HTTP Webserver",
        "AWS",
        "HTML",
        "CSS",
        "jQuery",
        "Bootstrap",
    ],
}

debug_path = None
error_path = None

if ENV == "local":
    debug_path = "./logs/debug.log"
    error_path = "./logs/error.log"
else:
    debug_path = "/home/ubuntu/logs/debug.log"
    error_path = "/home/ubuntu/logs/error.log"

LOGGING = {
    "version": 1,
    "loggers": {
        "django": {"handlers": ["debug_handler", "error_handler"], "level": "DEBUG",},
    },
    "handlers": {
        "debug_handler": {
            "level": "DEBUG",
            "class": "logging.handlers.RotatingFileHandler",
            "filename": debug_path,
            "backupCount": 10,
            "maxBytes": 5242880,
            "formatter": "formatter1",
        },
        "error_handler": {
            "level": "WARNING",
            "class": "logging.handlers.RotatingFileHandler",
            "filename": error_path,
            "backupCount": 10,
            "maxBytes": 5242880,
            "formatter": "formatter1",
        },
    },
    "formatters": {
        "formatter1": {"format": "\n{levelname} {asctime} \n{message}", "style": "{",}
    },
}
