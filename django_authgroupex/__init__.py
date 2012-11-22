# -*- coding: utf-8 -*-
# This code is distributed under the two-clause BSD license.
# Copyright (c) 2012 Raphaël Barrois


"""Provide a AuthGroupeX authentication backend for Django."""

from __future__ import absolute_import, unicode_literals


from .auth import AuthGroupeXBackend
from .auth import PERM_ADMIN, PERM_GROUP_ADMIN, PERM_GROUP_MEMBER, PERM_USER
from .exceptions import AuthGroupeXError, InvalidAuth
from .views import AuthGroupeXBaseView, AuthGroupeXUniqueView

__author__ = u"Raphaël Barrois <raphael.barrois@polytechnique.org>"
__version__ = '0.1.0'
