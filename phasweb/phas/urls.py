# -*- coding: utf-8 -*-
from django.conf.urls.defaults import *
from django.views.generic import *
from phas.models import *

urlpatterns = patterns('phas.views',
	# databases
	url(r'^database/$', list.ListView.as_view(
		model = Databases,
		template_name = 'databases/index.html',
		context_object_name = 'databases_list'
	)),
	url(r'^database/(?P<pk>\d+)/detail/$', edit.FormView.as_view(
		form_class = DatabasesForm,
		template_name = 'databases/detail.html'
	)),
	url(r'^database/(?P<database_id>\d+)/save/$', 'databases.save'),
)
