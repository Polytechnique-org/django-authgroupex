from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()
# Use authgroupex login on admin site
admin.site.login_template = 'authgroupex/admin_login.html'

urlpatterns = patterns('',
    url(r'^$', 'django_authgroupex_dev.devsite.views.home', name='home'),
    url(r'^xorgauth/', include('django_authgroupex.urls', namespace='authgroupex')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^logout/', 'django_authgroupex_dev.devsite.views.logout', name='logout'),
)
