# -*- coding: utf-8 -*-
from django.shortcuts import render_to_response, redirect
from django.http import Http404
from phas.models import *
from django.template import RequestContext

def index(request):
	return render_to_response('index.html', {
		'groups': Groups.objects.count(),
		'codes': len(Phas.objects.values_list('group_id', 'module').distinct()),
		'databases': Databases.objects.count(),
	})
