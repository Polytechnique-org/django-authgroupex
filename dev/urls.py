from django.conf.urls import patterns, include, url

import django_authgroupex
authgroupex_view = django_authgroupex.AuthGroupeXUniqueView()

from django.contrib import admin
admin.autodiscover()
# Use authgroupex login on admin site
admin.site.login_template = 'devsite/admin_login.html'

urlpatterns = patterns('',
    url(r'^$', 'dev.devsite.views.home', name='home'),
    url(r'^xorgauth/', authgroupex_view.login_view, name='xorgauth'),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^logout/', 'dev.devsite.views.logout', name='logout'),
)
