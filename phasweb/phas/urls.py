# -*- coding: utf-8 -*-
from django.conf.urls.defaults import *

urlpatterns = patterns('phas.views',
    url(r'^$', 'index'),
    url(r'^database/(?P<database_id>\d+)/$', 'detail'),
    url(r'^database/(?P<database_id>\d+)/save/$', 'save'),
)
