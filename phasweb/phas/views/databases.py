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
		'next_page': page.previous_page_number()
	})

def new(request):
	error_message = None
	if request.method == 'POST':
		database = Databases()
		form = DatabasesForm(request.POST, instance=database)
		if form.is_valid():
			form.save()
			return redirect('/database/')
		else:
			error_message = form.errors

	try:
		database = Databases()
		form = DatabasesForm(instance=database)
	except Databases.DoesNotExist:
		raise Http404
	return render_to_response('databases/edit.html', {
		'form': form,
		'database': database,
		'button': 'crear',
	}, context_instance=RequestContext(request))


def edit(request, database_id):
	error_message = None
	if request.method == 'POST':
		database = Databases.objects.get(pk=database_id)
		form = DatabasesForm(request.POST, instance=database)
		if form.is_valid():
			form.save()
		else:
			error_message = form.errors

	try:
		if database_id:
			database = Databases.objects.get(pk=database_id)
			form = DatabasesForm(instance=database)
		else:
			database = Databases()
			form = DatabasesForm(instance=database)
	except Databases.DoesNotExist:
		raise Http404
	return render_to_response('databases/edit.html', {
		'form': form,
		'database': database,
		'error_message': error_message,
		'button': 'modifica',
	}, context_instance=RequestContext(request))

def delete(request, database_id):
	Databases.objects.get(pk=database_id).delete()
	return redirect('/database/')
