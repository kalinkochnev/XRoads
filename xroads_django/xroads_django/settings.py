"""
Django settings for xroads_django project.

Generated by 'django-admin startproject' using Django 3.0.8.

For more information on this file, see
https://docs.djangoproject.com/en/3.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.0/ref/settings/
"""

import os

from django.urls import reverse_lazy

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
if (os.environ.get("SECRET_KEY","")!=""):
    SECRET_KEY = os.environ.get("SECRET_KEY")
else:
    SECRET_KEY = 'lp8q0qf++*#9oay4+15to5!=an!zn#6u-u8&amq&2y*r%=et3q'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = bool(os.environ.get("DJANGO_DEBUG",""))

# This needs to be set to the possible hostnames on which the backend runs
# e.g. if deployed to backend.xroads.com
ALLOWED_HOSTS = ["localhost","127.0.0.1"]
if (os.environ.get("ALLOWED_HOSTS","")!=""):
    ALLOWED_HOSTS = [ah.strip() for ah in os.environ.get("ALLOWED_HOSTS","").split(",")]


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # Rest app
    'XroadsAPI.apps.XroadsapiConfig',
    'XroadsAuth.apps.XroadsauthConfig',
    'rest_framework.authtoken',
    'dj_rest_auth',
    'rest_framework_nested',

    # Registration for dj-rest-auth
    'django.contrib.sites',
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'dj_rest_auth.registration',

    # JWT tokens
    'rest_framework_simplejwt',

    # documentation for api
    'drf_yasg',

    # cors headers
    'corsheaders',
]

run_mode = os.environ.get("RUN_MODE","DEV")
if (run_mode == "DEV"):
    # This is needed for django to run in SSL mode for local development - needed for cookies to 
    # work in the same way they work in production
    print("Running django in DEV_MODE, automatically adding sslserver app. If you see this in production, django will fail to start")
    INSTALLED_APPS.append("sslserver")
else:
    print("Running django in %s mode" % run_mode)



SITE_ID = 1

# Need for custom user model allauth
ACCOUNT_USER_MODEL_USERNAME_FIELD = None
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_USERNAME_REQUIRED = False
ACCOUNT_AUTHENTICATION_METHOD = 'email'

AUTHENTICATION_BACKENDS = [
    # Needed to login by username in Django admin, regardless of `allauth`
    'django.contrib.auth.backends.ModelBackend',

    # `allauth` specific authentication methods, such as login by e-mail
    'allauth.account.auth_backends.AuthenticationBackend',
]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'xroads_django.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
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

WSGI_APPLICATION = 'xroads_django.wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': os.environ.get("DB_NAME", "xroadsdb"),
        'USER': os.environ.get("DB_USER", 'djangouser'),
        'PASSWORD': os.environ.get("DB_PASS", "PTUvEj9Bh9P2"), 
        'HOST': os.environ.get("DB_HOST", "localhost"),
        'PORT': os.environ.get("DB_PORT", "5432")
    }
}


# Password validation
# Password validation
# https://docs.djangoproject.com/en/3.0/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/3.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.0/howto/static-files/

STATIC_URL = '/djstatic/'

# User substitution
# https://docs.djangoproject.com/en/1.11/topics/auth/customizing/#auth-custom-user
AUTH_USER_MODEL = 'XroadsAuth.Profile'

# Email for development only!!!
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
ACCOUNT_EMAIL_VERIFICATION = True
ACCOUNT_CONFIRM_EMAIL_ON_GET = True

ACCOUNT_LOGIN_ON_EMAIL_CONFIRMATION = False
LOGIN_URL = reverse_lazy("account_registration_success")
ACCOUNT_EMAIL_CONFIRMATION_AUTHENTICATED_REDIRECT_URL = LOGIN_URL
ACCOUNT_EMAIL_VERIFICATION = "mandatory"
ACCOUNT_EMAIL_CONFIRMATION_EXPIRE_DAYS = 7


# Base url to serve media files
MEDIA_URL = '/media/'

# Path where media is stored
MEDIA_ROOT = os.path.join(BASE_DIR, 'media/')

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'XroadsAuth.auth.CustomCookieAuthentication',
        
        # 'rest_framework_simplejwt.authentication.JWTAuthentication',
        # 'rest_framework.authentication.TokenAuthentication'
        # 'rest_framework.authentication.BasicAuthentication',
        # 'rest_framework.authentication.SessionAuthentication', # FIXME make sure to remove this in production
    ]
}

# JWT Token Settings
REST_USE_JWT = True
JWT_PAYLOAD_COOKIE_NAME = 'JWT-HEADER-PAYLOAD'
JWT_SIGNATURE_COOKIE_NAME = 'JWT-SIGNATURE'

from datetime import timedelta
ACCESS_TOKEN_LIFETIME = timedelta(days=7)
REFRESH_TOKEN_LIFETIME = timedelta(days=7)
JWT_AUTH = {
    # how long the original token is valid for
    'JWT_EXPIRATION_DELTA': ACCESS_TOKEN_LIFETIME,

    # allow refreshing of tokens
    'JWT_ALLOW_REFRESH': True,

    # this is the maximum time AFTER the token was issued that
    # it can be refreshed.  exprired tokens can't be refreshed.
    'JWT_REFRESH_EXPIRATION_DELTA': REFRESH_TOKEN_LIFETIME,
}

# Needed for dj-rest-auth
REST_AUTH_REGISTER_SERIALIZERS = {
    'REGISTER_SERIALIZER': 'XroadsAuth.serializers.CustomRegister',
}

REST_AUTH_SERIALIZERS = {
    'USER_DETAILS_SERIALIZER': 'XroadsAuth.serializers.ProfileSerializer',
}

SWAGGER_SETTINGS = {
    'USE_SESSION_AUTH': False,
}

# These are the settings involving emails
DJANGO_NO_REPLY = "no-reply@xroads.club"

#The root directory to collect static files
#STATIC_ROOT= os.path.join(BASE_DIR, '../deploy/staticfiles/')
STATIC_ROOT= os.path.join(BASE_DIR, './staticfiles/')

# CORS_ALLOW_ALL_ORIGINS=True 
# This setting configures the REST API to properly work when receiving
# requests from a cross-domain request. More specifically, when the frontend is running
# on one of these URLs, the backend will respond with proper CORS headers
# that allow the browser to interact across domain - e.g. 
# if the frontend is running on frontend.xroads.com and the backend is on 
# backend.xroads.com
if (os.environ.get("CORS_ALLOWED_ORIGINS","") == ""): 
    CORS_ALLOWED_ORIGINS = [
        "http://127.0.0.1:3000",
        "http://localhost:3000", 
        "https://localhost:3000",
        "https://127.0.0.1:3000"
    ]
else:
    CORS_ALLOWED_ORIGINS = [ o.strip() for o in os.environ.get("CORS_ALLOWED_ORIGINS","").split(",")]

# This allows the cookies to be received in the cross-domain requests, if the frontend
# is running on a different domain than the django app (e.g. if the frontend is running on 
# frontend.xroads.com and the backend is running on api.xroads.com)
CORS_ALLOW_CREDENTIALS=True    

# The domain for which the login cookie is set from the django backend. 
# For this domain (and if the domain starts with a '.', all of its subdomains), the browser
# will send cookies along with each request (thus allowing for the transparent authentication). 
# Additionally, if the frontend is running on a subdomain (e.g. react1.xroads.com), it will be able
# to see the login cookie and allow for proper login/logout. 
# ".xroads.com"
# 
JWT_COOKIE_DOMAIN=os.environ.get("JWT_COOKIE_DOMAIN","localhost")


# Settings for file/image storage in GCP
DEFAULT_FILE_STORAGE = 'storages.backends.gcloud.GoogleCloudStorage'
GS_BUCKET_NAME = 'xroads_django_files'
GS_PROJECT_ID="ak-xroads1"

# Collect static files into the bucket
STATICFILES_STORAGE = 'storages.backends.gcloud.GoogleCloudStorage'

from google.oauth2 import service_account

GS_CREDENTIALS = service_account.Credentials.from_service_account_file(
    "ak-xroads1-a86ad977fbb5.json"
)
