import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'p5y#gxf7#2-zt8-z%@l%am38bl$dp9@ehkd2eo0g#qzc&ln%by'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*',]
LOGIN_REDIRECT_URL = 'landing'
LOGIN_URL = 'login'

AUTHENTICATION_BACKENDS = (
    "django_python3_ldap.auth.LDAPBackend",
)

# LDAP auth settings.
LDAP_AUTH_URL = "#"

# Initiate TLS on connection.
LDAP_AUTH_USE_TLS = False

# The LDAP search base for looking up users.
LDAP_AUTH_SEARCH_BASE = "#"

# The LDAP class that represents a user.
LDAP_AUTH_OBJECT_CLASS = "inetOrgPerson"

# User model fields mapped to the LDAP
# attributes that represent them.
LDAP_AUTH_USER_FIELDS = {
    "username": "sAMAccountName",
    "first_name": "givenName",
    "last_name": "sn",
    "email": "mail",
}
LDAP_AUTH_OBJECT_CLASS = "user"

LDAP_AUTH_FORMAT_USERNAME = "django_python3_ldap.utils.format_username_active_directory"
LDAP_AUTH_ACTIVE_DIRECTORY_DOMAIN = "#"

LDAP_AUTH_CONNECTION_USERNAME = "#"
LDAP_AUTH_CONNECTION_PASSWORD = "#"


# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'crispy_forms',
    'users',
    'survey_app',
    'django_python3_ldap',
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

ROOT_URLCONF = 'logistics_scorecard_A.urls'

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

WSGI_APPLICATION = 'logistics_scorecard_A.wsgi.application'


# Database
# https://docs.djangoproject.com/en/2.2/ref/settings/#databases

DATABASES = {
   'default': {
       'ENGINE': 'django.db.backends.sqlite3',
       'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
   }
    # 'default': {
    #     'ENGINE': 'django.db.backends.oracle',
    #     'NAME': '#',
    #     'USER': '#',
    #     'PASSWORD': '#',
    #     'HOST': '#',
    #     'PORT': '#',
    # }

    #     'OPTIONS': {
    #         'driver': 'ODBC Driver 13 for SQL Server',
    #     },
    # },
}


# Password validation
# https://docs.djangoproject.com/en/2.2/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/2.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.2/howto/static-files/

STATIC_URL = '/static/'


CRISPY_TEMPLATE_PACK='bootstrap4'
