# -*- coding: utf-8 -*-
from django.shortcuts import render_to_response, redirect
from django.http import Http404
from phas.models import *
from phas.forms import *
from django.template import RequestContext
from django.core.paginator import Paginator, InvalidPage

def index(request, page_id = 1):
	page = int(page_id)
	groups = Paginator(Groups.objects.all(), 5)
	page = groups.page(page)
	return render_to_response('groups/index.html', {
		'groups': page.object_list,
		'has_prev': page.has_previous(),
		'has_next': page.has_next(),
		'prev_page': page.next_page_number(),
		'next_page': page.previous_page_number(),
		'pages': groups.page_range,
		'page_id': int(page_id),
		'titulo': 'Listado de Grupos',
		'tipo': 'folder',
	})

def edit(request, group_id=None):
	try:
		if group_id:
			group = Groups.objects.get(pk=group_id)
		else:
			group = Groups()
		if request.method == 'POST':
			form = GroupsForm(request.POST, instance=group, auto_id=False)
			if form.is_valid():
				form.save()
				return redirect('/group/')
		else:
			form = GroupsForm(instance=group, auto_id=False)
	except Groups.DoesNotExist:
		raise Http404

	return render_to_response('groups/edit.html', {
		'form': form,
		'group': group,
		'button': 'modifica' if group_id else 'crear',
		'forms': [{
			'id': 'group',
			'name': 'Grupo'
		}],
		'titulo': 'Edita Grupo' if group_id else 'Crea Grupo',
		'tipo': 'folder',
	}, context_instance=RequestContext(request))

def delete(request, group_id):
	Groups.objects.get(pk=group_id).delete()
	return redirect('/group/')
