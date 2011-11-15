# -*- coding: utf-8 -*-
from django.shortcuts import render_to_response, redirect
from django.http import Http404
from phas.models import *
from django.template import RequestContext

def index(request):
	return render_to_response('index.html', {
		'modules': Modules.objects.count(),
		'codes': len(Codes.objects.values_list('module_id', 'name').distinct()),
		'databases': Databases.objects.count(),
		'tads': TAD.objects.exclude(tad_type='S').count(),
	})
