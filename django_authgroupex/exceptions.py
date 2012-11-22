# -*- coding: utf-8 -*-
# This code is distributed under the two-clause BSD license.
# Copyright (c) 2012 Raphaël Barrois

from __future__ import absolute_import, unicode_literals


class AuthGroupeXError(Exception):
    """Base class for AuthGroupeX errors."""


class ProcessError(AuthGroupeXError):
    """Raised when an error occured in the request-response process."""


class InvalidAuth(ProcessError):
    """Raised when the 'auth' field of a response was invalid."""


class UsernameViolation(AuthGroupeXError):
    """Raised when an invalid username was submitted."""

