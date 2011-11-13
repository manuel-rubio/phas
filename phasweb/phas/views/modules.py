# -*- coding: utf-8 -*-
from django.shortcuts import render_to_response, redirect
from django.http import Http404
from phas.models import *
from phas.forms import *
from django.template import RequestContext
from django.core.paginator import Paginator, InvalidPage

def index(request, page_id = 1):
	page = int(page_id)
	modules = Paginator(Modules.objects.all(), 5)
	page = modules.page(page)
	return render_to_response('modules/index.html', {
		'modules': page.object_list,
		'has_prev': page.has_previous(),
		'has_next': page.has_next(),
		'prev_page': page.next_page_number(),
		'next_page': page.previous_page_number(),
		'pages': modules.page_range,
		'page_id': int(page_id),
		'titulo': 'Listado de Modulos',
		'tipo': 'folder',
	})

def edit(request, module_id=None):
	try:
		if module_id:
			module = Modules.objects.get(pk=module_id)
		else:
			module = Modules()
		if request.method == 'POST':
			form = ModulesForm(request.POST, instance=module, auto_id=False)
			if form.is_valid():
				form.save()
				return redirect('/module/')
		else:
			form = ModulesForm(instance=module, auto_id=False)
	except Modules.DoesNotExist:
		raise Http404

	return render_to_response('modules/edit.html', {
		'form': form,
		'module': module,
		'button': 'modifica' if module_id else 'crear',
		'forms': [{
			'id': 'module',
			'name': 'Módulo'
		}],
		'titulo': 'Edita Módulo' if module_id else 'Crea Módulo',
		'tipo': 'folder',
	}, context_instance=RequestContext(request))

def delete(request, module_id):
	Modules.objects.get(pk=module_id).delete()
	return redirect('/module/')
