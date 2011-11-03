# -*- coding: utf-8 -*-
from django.shortcuts import render_to_response, redirect
from django.http import Http404
from phas.models import *
from phas.forms import *
from django.template import RequestContext
from django.core.paginator import Paginator, InvalidPage

def index(request, page_id = 1):
	page = int(page_id)
	codes = Paginator(Phas.objects.all(), 5)
	page = codes.page(page)
	return render_to_response('codes/index.html', {
		'codes': page.object_list,
		'has_prev': page.has_previous(),
		'has_next': page.has_next(),
		'prev_page': page.next_page_number(),
		'next_page': page.previous_page_number(),
		'pages': codes.page_range,
		'page_id': int(page_id),
		'titulo': 'Listado de Códigos',
		'tipo': 'config',
	})
	
def edit(request, code_id=None):
	try:
		if code_id:
			code = Phas.objects.get(pk=code_id)
		else:
			code = Phas()
		if request.method == 'POST':
			form = PhasForm(request.POST, instance=code, auto_id=False)
			if form.is_valid():
				form.save()
				return redirect('/code/')
		else:
			form = PhasForm(instance=code, auto_id=False)
	except Phas.DoesNotExist:
		raise Http404

	return render_to_response('codes/edit.html', {
		'form': form,
		'code': code,
		'button': 'modifica' if code_id else 'crear',
		'forms': [{
			'id': 'code',
			'name': 'Código'
		}],
		'titulo': 'Edita Código' if code_id else 'Crea Código',
		'tipo': 'config',
	}, context_instance=RequestContext(request))

def delete(request, code_id):
	Phas.objects.get(pk=code_id).delete()
	return redirect('/code/')
