# -*- coding: utf-8 -*-
# This code is distributed under the two-clause BSD license.
# Copyright (c) 2012-2013 Raphaël Barrois

from __future__ import absolute_import, unicode_literals


from django.conf import settings

import appconf


class AuthGroupeXConf(appconf.AppConf):
    """Global, django-appconf based config for authgroupex."""

    # Pre-shared key for authenticating our site to remote
    KEY = ''

    # Url of the endpoint
    ENDPOINT = 'https://www.polytechnique.org/auth-groupex/utf8'

    # Return URL where the AuthGroupeX server should user back
    RETURN_URL = ''
    def configure_return_url(self, value):
        return value or settings.LOGIN_URL

    # Fields to fetch from remote; order matters.
    FIELDS = ('username', 'firstname', 'lastname', 'email')

    # The AuthGroupeX permissions that enable the 'is_admin' flag on this site
    SUPERADMIN_PERMS = ()

    # The AuthGroupeX permissions that enable the 'is_staff' flag on this site
    STAFF_PERMS = ()

    # Whether accounts for now-dead users should switch to is_active=False
    DISABLE_DEADS = False

    # Name of the group to query as
    GROUP = ''

    # Maps a auth-groupex perm to a local group name
    MAP_GROUPS = {}

    # Model to store users to
    USER_MODEL = 'auth.User'

    # Group to store groups to
    GROUP_MODEL = 'auth.Group'

    class Meta:
        prefix = 'authgroupex'
        # Forward setting lookups to base django.conf.settings
        proxy = True
