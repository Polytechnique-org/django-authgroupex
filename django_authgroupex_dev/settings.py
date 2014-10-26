"""
Django settings for django_authgroupex_dev project.

For more information on this file, see
https://docs.djangoproject.com/en/1.7/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.7/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
BASE_DIR = os.path.abspath(os.path.dirname(__file__))

def read_pass(name):
    fname = os.path.join(BASE_DIR, 'private', name)
    with open(fname, 'r') as f:
        return f.readline().strip()

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.7/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'DEV ONLY !!'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

TEMPLATE_DEBUG = True

ALLOWED_HOSTS = ['127.0.0.1', '[::1]', 'localhost']


# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'django_authgroupex',
    'django_authgroupex_dev.devsite',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'django_authgroupex_dev.urls'

WSGI_APPLICATION = 'django_authgroupex_dev.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.7/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

# Internationalization
# https://docs.djangoproject.com/en/1.7/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Europe/Paris'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.7/howto/static-files/

STATIC_URL = '/static/'

# Absolute path to the directory static files should be collected to.
# Don't put anything in this directory yourself; store your static files
# in apps' "static/" subdirectories and in STATICFILES_DIRS.
# Example: "/home/media/media.lawrence.com/static/"
STATIC_ROOT = ''

AUTHENTICATION_BACKENDS = (
    'django_authgroupex.auth.AuthGroupeXBackend',
)
AUTHGROUPEX_KEY = read_pass('authgroupex.key')
AUTHGROUPEX_FIELDS = ('username', 'firstname', 'lastname', 'email', 'promo', 'perms', 'grpauth')
AUTHGROUPEX_FAKE = True
AUTHGROUPEX_ENDPOINT = 'authgroupex:fake_endpoint'
LOGIN_URL = '/xorgauth/'
LOGIN_REDIRECT_URL = '/'

# When using a site dedicated to a group, make the members "staff" and the admins "admin"
AUTHGROUPEX_GROUP = 'Polytechnique.org'
AUTHGROUPEX_SUPERADMIN_PERMS = ('admin', 'grpadmin')
AUTHGROUPEX_STAFF_PERMS = ('grpmember',)

AUTHGROUPEX_FAKE_ACCOUNTS = (
    {
        'displayname': 'Admin Istrateur (global admin)',
        'username': 'admin.istrateur.1942',
        'firstname': 'Admin',
        'lastname': 'Istrateur',
        'email': 'admin.istrateur.1942@polytechnique.org',
        'promo': '1942',
        'perms': 'admin',
        'grpauth': '',
    },
    {
        'displayname': 'Presi Dent (group admin)',
        'username': 'presi.dent.1901',
        'firstname': 'Presi',
        'lastname': 'Dent',
        'email': 'presi.dent.1901@polytechnique.org',
        'promo': '1901',
        'perms': 'user',
        'grpauth': 'admin',
    },
    {
        'displayname': 'Mem Ber (group member)',
        'username': 'mem.ber.1902',
        'firstname': 'Mem',
        'lastname': 'Ber',
        'email': 'mem.ber.1902@polytechnique.org',
        'promo': '1902',
        'perms': 'user',
        'grpauth': 'membre',
    },
    {
        'displayname': 'Lambda User (not admin, not group member)',
        'username': 'lambda.user.1922',
        'firstname': 'Lambda',
        'lastname': 'User',
        'email': 'mem.ber.1922@polytechnique.org',
        'promo': '1922',
        'perms': 'user',
        'grpauth': '',
    },
)

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
)

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
)


TEMPLATE_DIRS = (
    # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
)

# A sample logging configuration. The only tangible logging
# performed by this configuration is to send an email to
# the site admins on every HTTP 500 error when DEBUG=False.
# See http://docs.djangoproject.com/en/dev/topics/logging for
# more details on how to customize your logging configuration.
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        }
    },
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler'
        }
    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
    }
}
