# -*- coding: utf-8 -*-
from django.conf.urls.defaults import *
from django.views.generic import *
from phas.models import *
from phas.forms import *

urlpatterns = patterns('phas.views',
	url(r'^$', 'base.index'),

	url(r'^database/$', 'databases.index'),
	url(r'^database/(?P<page_id>\d+)/$', 'databases.index'),
	url(r'^database/(?P<database_id>\d+)/edit/$', 'databases.edit'),
	url(r'^database/(?P<database_id>\d+)/delete/$', 'databases.delete'),
	url(r'^database/new/$', 'databases.edit'),

	url(r'^module/$', 'modules.index'),
	url(r'^module/(?P<page_id>\d+)/$', 'modules.index'),
	url(r'^module/(?P<module_id>\d+)/edit/$', 'modules.edit'),
	url(r'^module/(?P<module_id>\d+)/delete/$', 'modules.delete'),
	url(r'^module/new/$', 'modules.edit'),

	url(r'^code/$', 'codes.index'),
	url(r'^code/(?P<page_id>\d+)/$', 'codes.index'),
	url(r'^code/(?P<code_id>\d+)/edit/$', 'codes.edit'),
	url(r'^code/(?P<code_id>\d+)/delete/$', 'codes.delete'),
	url(r'^code/new/$', 'codes.edit'),
	url(r'^code/(?P<code_id>\d+)/diff/$', 'codes.diff'),
	url(r'^code/(?P<code_id>\d+)/diff/(?P<src>\d+)/(?P<dst>\d+)/$', 'codes.diff'),
	url(r'^code/(?P<code_id>\d+)/publish/$', 'codes.publish'),

	url(r'^soap/$', 'soap.index'),
	url(r'^soap/(?P<page_id>\d+)/$', 'soap.index'),
	url(r'^soap/(?P<tad_id>\d+)/edit/$', 'soap.edit'),
	url(r'^soap/(?P<tad_id>\d+)/delete/$', 'soap.delete'),
	url(r'^soap/new/$', 'soap.edit'),
)
