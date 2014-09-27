#!/usr/bin/env python

import sys

import django
from django.conf import settings

if not settings.configured:
    settings.configure(
        AUTHENTICATION_BACKENDS=(
            'django_authgroupex.auth.AuthGroupeXBackend',
        ),
        DATABASES={
            'default': {
                'ENGINE': 'django.db.backends.sqlite3',
                'NAME': ':memory:',
            }
        },
        INSTALLED_APPS=(
            'django.contrib.auth',
            'django.contrib.contenttypes',
            'django.contrib.messages',
            'django.contrib.sessions',
            'django.contrib.sites',
            'django_authgroupex',
        ),
        SITE_ID=1,
        SECRET_KEY='this-is-just-for-tests-so-not-that-secret',
        TEST_RUNNER = 'django.test.simple.DjangoTestSuiteRunner',
        AUTHGROUPEX_LOGIN_REDIRECT_URL='/login-success/',
        MIDDLEWARE_CLASSES=()
    )



from django.test.utils import get_runner


def runtests():
    if hasattr(django, 'setup'):
        django.setup()
    apps = ['django_authgroupex', ]
    TestRunner = get_runner(settings)
    test_runner = TestRunner(verbosity=1, interactive=True, failfast=False)
    failures = test_runner.run_tests(apps)
    sys.exit(failures)


if __name__ == '__main__':
    runtests()
