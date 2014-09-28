# -*- coding: utf-8 -*-
# This code is distributed under the two-clause BSD license.
# Copyright (c) 2012-2013 Raphaël Barrois

from __future__ import absolute_import, unicode_literals


from django.conf import settings

import appconf


class AuthGroupeXConf(appconf.AppConf):
    """Global, django-appconf based config for authgroupex."""

    class Meta:
        prefix = 'authgroupex'

    # Pre-shared key for authenticating our site to remote
    KEY = ''

    # Url of the endpoint
    ENDPOINT = 'https://www.polytechnique.org/auth-groupex/utf8'

    # Return URL where the AuthGroupeX server should send back the user-agent
    RETURN_URL = ''
    def configure_return_url(self, value):
        return value or settings.LOGIN_URL

    # Redirection URL post-authgroupex if no next= view was set.
    LOGIN_REDIRECT_URL = ''
    def config_login_redirect_url(self, value):
        return value or settings.LOGIN_REDIRECT_URL

    # Fields to fetch from remote; order matters.
    FIELDS = ('username', 'firstname', 'lastname', 'email')

    # The AuthGroupeX permissions that enable the 'is_admin' flag on this site
    SUPERADMIN_PERMS = ()

    # The AuthGroupeX permissions that enable the 'is_staff' flag on this site
    STAFF_PERMS = ()

    # Maps a auth-groupex perm to a local group name
    MAP_GROUPS = {}

    # Whether accounts for now-dead users should switch to is_active=False
    DISABLE_DEADS = False

    # Name of the 'GroupeX' to query ENDPOINT as
    GROUP = ''

    # Model to store users to
    USER_MODEL = ''
    def configure_user_model(self, value):
        return value or getattr(settings, 'AUTH_USER_MODEL', '') or 'auth.User'

    # Group to store groups to
    GROUP_MODEL = 'auth.Group'

    # Whether to enable the fake endpoint for debugging purpose
    # True means "always", False "never" and None "only when DEBUG is active"
    FAKE = None
    def configure_fake(self, value):
        return settings.DEBUG if value is None else value

    # Preset accounts for the fake endpoint
    FAKE_ACCOUNTS = ()
