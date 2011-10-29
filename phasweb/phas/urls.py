# -*- coding: utf-8 -*-
from django.conf.urls.defaults import *
from django.views.generic import *
from phas.models import *
from phas.forms import *

urlpatterns = patterns('phas.views',
	url(r'^database/$', 'databases.index'),
	url(r'^database/(?P<page_id>\d+)/$', 'databases.index'),
	url(r'^database/(?P<database_id>\d+)/edit/$', 'databases.edit'),
	url(r'^database/(?P<database_id>\d+)/delete/$', 'databases.delete'),
	url(r'^database/new/$', 'databases.new'),
)
