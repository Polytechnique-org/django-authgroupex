# -*- coding: utf-8 -*-

from __future__ import unicode_literals

import hashlib
import sys

# handle changements from python2 to python3
if sys.version_info[0] <= 2:
    import urlparse as urllib_parse
else:
    from urllib import parse as urllib_parse


from django.contrib.auth.models import User
from django.contrib.sessions.middleware import SessionMiddleware
from django.contrib.auth.middleware import AuthenticationMiddleware
from django.test import TestCase
from django.test.client import RequestFactory
from django.test.utils import override_settings

from django_authgroupex import conf as groupex_conf
from django_authgroupex import views as groupex_views

@override_settings(AUTHENTICATION_BACKENDS=('django_authgroupex.auth.AuthGroupeXBackend',))
class AuthGroupeXViewsTestCase(TestCase):
    def setUp(self):
        super(AuthGroupeXViewsTestCase, self).setUp()
        self.config = groupex_conf.AuthGroupeXConf()
        self.unique_view = groupex_views.AuthGroupeXUniqueView()
        # factory needed by all tests
        self.factory = RequestFactory()

    def _get_with_session(self, url):
        """Creates request object with a session."""
        request = self.factory.get(url)
        SessionMiddleware().process_request(request)
        request.session.save()
        return request

    def test_begin_view(self):
        """Login view should redirect to polytechnique.org with appropriate GET arguments."""
        request = self._get_with_session('/accounts/login/')
        response = self.unique_view.login_view(request)
        # check if redirection
        self.assertIn('location', response._headers)
        # check validity of redirection
        url = response._headers['location'][1]
        self.assertEqual(url[:48],"https://www.polytechnique.org/auth-groupex/utf8?")
        # check get data
        challenge = request.session['authgroupex-challenge']
        get_dict = dict(urllib_parse.parse_qsl(url[48:]))
        self.assertEquals(get_dict['challenge'], challenge)
        self.assertEquals(get_dict['pass'], hashlib.md5((challenge + self.config.KEY).encode('ascii')).hexdigest())
        self.assertEquals(get_dict['url'], 'http://testserver/accounts/login/?auth_groupex_return=1')

    def test_return_view(self):
        """Return view should be handled properly and create a user."""
        # first, we need a request with a challenge
        begin_request = self._get_with_session('/accounts/login/')
        self.unique_view.login_view(begin_request)
        challenge = begin_request.session['authgroupex-challenge']
        # now, the real request
        check_str = (
            '1' + challenge + self.config.KEY + 'paul.dupond.2011PaulDupondpaul.dupond@polytechnique.org1'
            ).encode('utf-8')
        request = self._get_with_session(
            '/accounts/login/?auth_groupex_return=1&username=paul.dupond.2011'
            '&firstname=Paul&lastname=Dupond&email=paul.dupond@polytechnique.org'
            '&challenge=' + challenge + '&auth=' + hashlib.md5(check_str).hexdigest()
            )
        request.session['authgroupex-challenge'] = challenge
        response = self.unique_view.login_view(request)
        # check status code
        self.assertEquals(response.status_code, 302)
        # check the user is indeed authenticated
        AuthenticationMiddleware().process_request(request)
        self.assertEquals(request.user, User.objects.get(username='paul.dupond.2011'))
