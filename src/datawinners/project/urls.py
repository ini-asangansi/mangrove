# vim: ai ts=4 sts=4 et sw=4 encoding=utf-8
from django.conf.urls.defaults import patterns
from datawinners.project.views import questionnaire

urlpatterns = patterns('',
    (r'^project/questionnaire', questionnaire),
)