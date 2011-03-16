from django.conf.urls.defaults import patterns, include, url
import os
from settings import PROJECT_DIR

urlpatterns = patterns('',
    (r'',include('web.login.urls')),
    # Examples:
    # url(r'^$', 'web.views.home', name='home'),
    # url(r'^web/', include('web.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
)