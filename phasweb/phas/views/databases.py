# -*- coding: utf-8 -*-
from django.shortcuts import render_to_response, redirect
from django.http import Http404
from phas.models import *
from phas.forms import *
from django.template import RequestContext
from django.core.paginator import Paginator, InvalidPage

def index(request, page_id = 1):
	page = int(page_id)
	databases = Paginator(Databases.objects.all(), 5)
	page = databases.page(page)
	return render_to_response('databases/index.html', {
		'databases': page.object_list,
		'has_prev': page.has_previous(),
		'has_next': page.has_next(),
		'prev_page': page.next_page_number(),
		'next_page': page.previous_page_number(),
		'pages': databases.page_range,
		'page_id': int(page_id),
		'titulo': 'Listado de Databases',
		'tipo': 'database',
	})

def edit(request, database_id=None):
	try:
		if database_id:
			database = Databases.objects.get(pk=database_id)
		else:
			database = Databases()
		if request.method == 'POST':
			form = DatabasesForm(request.POST, instance=database, auto_id=False)
			if form.is_valid():
				form.save()
				return redirect('/database/')
		else:
			form = DatabasesForm(instance=database, auto_id=False)
	except Databases.DoesNotExist:
		raise Http404

	return render_to_response('databases/edit.html', {
		'form': form,
		'database': database,
		'button': 'modifica' if database_id else 'crear',
		'forms': [{
			'id': 'database',
			'name': 'Database'
		}],
		'titulo': 'Edita Database' if database_id else 'Crea Database',
		'tipo': 'database',
	}, context_instance=RequestContext(request))

def delete(request, database_id):
	Databases.objects.get(pk=database_id).delete()
	return redirect('/database/')
