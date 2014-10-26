# -*- coding: utf-8 -*-
# This code is distributed under the two-clause BSD license.
# Copyright (c) 2012-2013 Raphaël Barrois

from __future__ import absolute_import, unicode_literals


import hashlib
import random
import struct

from django import http
from django.contrib import auth as django_auth
from django.core.urlresolvers import reverse

from . import auth
from . import conf
from . import exceptions


class URLFormatter(object):
    """Handles URL formatting and parsing."""

    def __init__(self, config=None, *args, **kwargs):
        super(URLFormatter, self).__init__(*args, **kwargs)
        self.config = config or conf.AuthGroupeXConf()

    def make_url(self, request, return_url=None):
        """Compute the remote URL.

        Args:
            request: http.HttpRequest, the request to use for session storage
                and current URL retrieving
            return_url: str, the optional return URL to use; if empty, the
                current URL of the request will be used.

        Returns:
            the new url.
        """
        challenge = hashlib.sha1(
                b''.join(struct.pack(b'B', random.randrange(0, 256)) for i in range(64)))
        challenge = challenge.hexdigest()

        request.session['authgroupex-challenge'] = challenge

        sig = hashlib.md5((challenge + self.config.KEY).encode('ascii')).hexdigest()
        query = http.QueryDict('', mutable=True)
        query['challenge'] = challenge
        query['pass'] = sig
        query['url'] = request.build_absolute_uri(return_url)
        if self.config.GROUP:
            query['group'] = self.config.GROUP

        endpoint = self.config.ENDPOINT
        if self.config.FAKE:
            endpoint = reverse(endpoint)

        url = endpoint + '?' + query.urlencode()
        return url

    def parse_return(self, request):
        """Parse the returned data.

        Args:
            request: the request received on the return URL

        Returns:
            An AuthResult object.
        """
        if 'auth' not in request.GET:
            raise exceptions.InvalidAuth("request.GET lacks a 'auth' field.")

        if 'authgroupex-challenge' not in request.session:
            raise exceptions.InvalidAuth(
                    "request.session lacks a 'authgroupex-challenge' field.")

        data = {}
        check_str = '1{challenge}{key}'.format(
                challenge=request.session['authgroupex-challenge'],
                key=self.config.KEY)

        for field in self.config.FIELDS:
            if field not in request.GET:
                raise exceptions.InvalidAuth(
                    "request.GET lacks a '{}' field.".format(field))
            data[field] = request.GET[field]
            check_str += data[field]

        check_str += '1'
        check_str = check_str.encode('utf-8')
        if hashlib.md5(check_str).hexdigest() != request.GET['auth']:
            raise exceptions.InvalidAuth(
                    "Invalid signature in authgroupex response.")

        return auth.AuthResult(data=data)


# Expected behaviour:
# 1) User goes to /foobar/
# 2) The view for /foobar/ has a @login_required decorator
# 3) @login_required redirects to <LOGIN_URL>?next=/foobar/
# 4) (optionnally) the user clicks on a link that brings him to AuthGroupeXBaseView.login_begin_view with ?next=/foobar/
# 5) AuthGroupeXBaseView.login_begin_view redirects to https://x.org/...&url=AuthGroupeXBaseView.login_return_view?next=/foobar/
# 6) X.org authenticates and redirects to AuthGroupeXBaseView.login_return_view?user=..&next=/foobar/
# 7) AuthGroupeXBaseView.login_return_view sends to /foobar/


class AuthGroupeXBaseView(object):
    """Base view class to use for login.

    Provides separated 'login' and 'return' views.
    """

    def __init__(self, url_formatter=None, config=None, *args, **kwargs):
        super(AuthGroupeXBaseView, self).__init__(*args, **kwargs)
        self.config = config or conf.AuthGroupeXConf()
        self.url_formatter = url_formatter or URLFormatter(self.config)
        self.include_return_param = False

    # We need to redefine builtin 'next'
    # pylint: disable=W0622
    def build_return_url(self, request, next=None):
        """Builds the return URL for a request."""
        url = self.config.RETURN_URL
        query = http.QueryDict('', mutable=True)
        if next:
            query['next'] = next

        if self.include_return_param:
            query['auth_groupex_return'] = '1'

        url += '?' + query.urlencode()
        return self.url_formatter.make_url(request, url)

    def login_begin_view(self, request, next=None):
        """View initiating the authgroupex authentication."""
        next = next or request.GET.get('next')
        auth_url = self.build_return_url(request, next)
        return http.HttpResponseRedirect(auth_url)

    def admin_login(self, request, extra_context=None):
        """View to use instead of the standard admin login page."""
        return self.login_begin_view(request, next=request.get_full_path())
    # pylint: enable=W0622

    def login_return_view(self, request):
        """View handling the 'return' data from authgroupex."""
        data = self.url_formatter.parse_return(request)
        user = django_auth.authenticate(authgroupex=data)
        if user and user.is_active:
            django_auth.login(request, user)
            if 'next' in request.GET:
                redirect_to = request.GET['next']
            else:
                redirect_to = self.config.LOGIN_REDIRECT_URL

            return http.HttpResponseRedirect(redirect_to)
        else:
            return http.HttpResponse('Internal error.', status=500)


class AuthGroupeXUniqueView(AuthGroupeXBaseView):
    """View class providing a unified login/return view."""

    def __init__(self, *args, **kwargs):
        super(AuthGroupeXUniqueView, self).__init__(*args, **kwargs)
        self.include_return_param = True

    # We need to redefine builtin 'next'
    # pylint: disable=W0622
    def login_view(self, request, next=None):
        """View dispatching the request to the adequate processing view."""
        if request.GET.get('auth_groupex_return') == '1':
            return self.login_return_view(request)
        else:
            return self.login_begin_view(request, next)
    # pylint: enable=W0622
