#!/usr/bin/env python
# -*- coding: utf-8 -*-
# This code is distributed under the two-clause BSD license.
# Copyright (c) 2012-2013 Raphaël Barrois

import codecs
import os
import re
import sys

from setuptools import setup
from distutils import cmd

root = os.path.abspath(os.path.dirname(__file__))

def get_version(*module_dir_components):
    version_re = re.compile(r"^__version__ = ['\"](.*)['\"]$")
    module_root = os.path.join(root, *module_dir_components)
    module_init = os.path.join(module_root, '__init__.py')
    with codecs.open(module_init, 'r', 'utf-8') as f:
        for line in f:
            match = version_re.match(line[:-1])
            if match:
                return match.groups()[0]
    return '0.1.0'


PACKAGE = 'django_authgroupex'
VERSION = get_version(PACKAGE)


setup(
    name="django_authgroupex",
    version=VERSION,
    description="An authentication backend for Django based on Polytechnique.org's auth-groupe-x SSO protocol.",
    author="Raphaël Barrois",
    author_email="raphael.barrois+djauthgroupex@polytechnique.org",
    url='https://github.com/Polytechnique-org/django-authgroupex',
    download_url='http://pypi.python.org/pypi/django-authgroupex/',
    keywords=['sso', 'authentication', 'django', 'authgroupex'],
    packages=['django_authgroupex', 'django_authgroupex.fake'],
    package_data={
        'django_authgroupex': [
            os.path.join('templates', 'authgroupex', '*.html'),
            os.path.join('static', 'authgroupex', '*.js'),
            os.path.join('static', 'authgroupex', '*.css'),
        ],
    },
    license='BSD',
    setup_requires=[
        'setuptools>=0.8',
    ],
    install_requires=[
        'Django>=1.3',
        'django_appconf',
    ],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
    ],
    test_suite = "runtests.runtests",
)
