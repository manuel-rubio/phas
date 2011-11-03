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
	url(r'^database/new/$', 'databases.edit'),

	url(r'^group/$', 'groups.index'),
	url(r'^group/(?P<page_id>\d+)/$', 'groups.index'),
	url(r'^group/(?P<group_id>\d+)/edit/$', 'groups.edit'),
	url(r'^group/(?P<group_id>\d+)/delete/$', 'groups.delete'),
	url(r'^group/new/$', 'groups.edit'),

	url(r'^code/$', 'codes.index'),
	url(r'^code/(?P<code_id>\d+)/$', 'codes.index'),
	url(r'^code/(?P<code_id>\d+)/edit/$', 'codes.edit'),
	url(r'^code/(?P<code_id>\d+)/delete/$', 'codes.delete'),
	url(r'^code/new/$', 'codes.edit'),
)
