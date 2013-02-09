from django.conf.urls import patterns, url

from . import conf
from . import views


urlpatterns = patterns('',
    url(r'^$', views.AuthGroupeXUniqueView().login_view, name='login'),
)


config = conf.AuthGroupeXConf()

if config.FAKE:
    urlpatterns += patterns('django_authgroupex.fake.views',
        url(r'^fake/validate/$', 'endpoint', name='fake_endpoint'),
        url(r'^fake/fill/$', 'login_view', name='fake_fill'),
    )
