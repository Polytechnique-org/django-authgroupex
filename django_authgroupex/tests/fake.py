# -*- coding: utf-8 -*-

from django.contrib.auth.models import User
from django.contrib.sessions.middleware import SessionMiddleware
from django.contrib.messages.middleware import MessageMiddleware
from django.conf.urls import patterns, include, url
from django.test import TestCase
from django.test.client import RequestFactory
from django.test.utils import override_settings

from django_authgroupex.fake import views as fake_views
from django_authgroupex import views as groupex_views
from django_authgroupex import conf as groupex_conf

class TestFakeUrls:
    urlpatterns = patterns('django_authgroupex.fake.views',
        url(r'^$', groupex_views.AuthGroupeXUniqueView().login_view, name='login'),
        url(r'^fake/validate/$', 'endpoint', name='fake_endpoint'),
        url(r'^fake/fill/$', 'login_view', name='fake_fill'),
    )

class TestUrls:
    urlpatterns = patterns('',
        url(r'^xorgauth/', include(TestFakeUrls, namespace='authgroupex')),
    )

@override_settings(ROOT_URLCONF=TestUrls)
class AuthGroupeXFakeTestCase(TestCase):

    def setUp(self):
        super(AuthGroupeXFakeTestCase, self).setUp()
        self.factory = RequestFactory()
        self.config = groupex_conf.AuthGroupeXConf()
        self.config.FAKE = True
        self.config.ENDPOINT = "authgroupex:fake_endpoint"
        self.unique_view = groupex_views.AuthGroupeXUniqueView(config=self.config)

    def _apply_middlewares(self, request):
        """Applies needed middlewares."""
        SessionMiddleware().process_request(request)
        MessageMiddleware().process_request(request)
        request.session.save()
        return request

    def test_fake_login(self):
        # fake redirection
        request = self._apply_middlewares(self.factory.get('/accounts/login/'))
        response = self.unique_view.login_view(request)
        challenge = request.session['authgroupex-challenge'] #  store it for later

        # test endpoint
        remote_url = response.get('location')
        response = fake_views.endpoint(self._apply_middlewares(self.factory.get(remote_url)))
        self.assertEquals(response.status_code, 302)

        # posting fake data
        post_data = {
            'username': 'jean.michel.2008',
            'firstname': 'Jean',
            'lastname': 'Michel',
            'email': 'jean.michel@polytechnique.org'
        }
        request = self._apply_middlewares(self.factory.post(remote_url, post_data))
        response = fake_views.login_view(request)
        self.assertEquals(response.status_code, 302)

        # make sure fake data creates the correct user
        redirect_url = response._headers['location'][1]
        request = self._apply_middlewares(self.factory.get(redirect_url))
        request.session['authgroupex-challenge'] = challenge
        response = self.unique_view.login_view(request)
        self.assertEquals(response.status_code, 302)
        self.assertEquals(response.get('Location'), self.config.LOGIN_REDIRECT_URL)

        user = User.objects.get(username='jean.michel.2008')
        self.assertEquals(user.first_name, 'Jean')
        self.assertEquals(user.last_name, 'Michel')
        self.assertEquals(user.email, 'jean.michel@polytechnique.org')
