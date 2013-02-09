#!/usr/bin/env python
# -*- coding: utf-8 -*-
# This code is distributed under the two-clause BSD license.
# Copyright (c) 2012-2013 Raphaël Barrois

from setuptools import setup
import os
import re

root_dir = os.path.abspath(os.path.dirname(__file__))


def get_version(package_name):
    version_re = re.compile(r"^__version__ = [\"']([\w_.-]+)[\"']$")
    package_components = package_name.split('.')
    path_components = package_components + ['__init__.py']
    with open(os.path.join(root_dir, *path_components)) as f:
        for line in f:
            match = version_re.match(line[:-1])
            if match:
                return match.groups()[0]
    return '0.1.0'


PACKAGE = 'django_authgroupex'


setup(
    name="django_authgroupex",
    version=get_version(PACKAGE),
    author="Raphaël Barrois",
    author_email="raphael.barrois@polytechnique.org",
    description="An authentication backend for Django based on Polytechnique.org's auth-groupe-x SSO protocol.",
    license="BSD",
    keywords=['sso', 'authentication', 'django', 'authgroupex'],
    url="http://github.com/rbarrois/django-authgroupex",
    download_url="http://pypi.python.org/pypi/django-authgroupex/",
    packages=['django_authgroupex', 'django_authgroupex.fake'],
    include_package_data=True,
    setup_requires=[
        'distribute',
    ],
    install_requires=[
        'Django',
        'django-appconf',
    ],
    classifiers=[
        "Development Status :: 4 - Beta",
        "Framework :: Django",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: BSD License",
        "Topic :: Software Development :: Libraries :: Python Modules",
        'Operating System :: OS Independent',
        'Programming Language :: Python',
    ],
    test_suite='tests',
)

