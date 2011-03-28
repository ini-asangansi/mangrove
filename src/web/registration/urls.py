from django.conf.urls.defaults import patterns, include, url
from web.registration.forms import NGOLoginForm
from web.registration.views import *

urlpatterns = patterns('',
    ('login', 'django.contrib.auth.views.login', {'authentication_form': NGOLoginForm}),
    ('register', register),
    ('home', home),
    # Examples:
    # url(r'^$', 'web.views.home', name='home'),
    # url(r'^web/', include('web.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
)
