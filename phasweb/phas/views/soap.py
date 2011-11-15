# -*- coding: utf-8 -*-
from django.shortcuts import render_to_response, redirect
from django.http import Http404
from phas.models import *
from phas.forms import *
from django.template import RequestContext
from django.core.paginator import Paginator, InvalidPage
from datetime import *

def index(request, page_id = 1):
    tads = Paginator(TAD.objects.exclude(tad_type='S'), 5)
    page = tads.page(int(page_id))
    return render_to_response('soap/index.html', {
        'tads': page.object_list,
        'has_prev': page.has_previous(),
        'has_next': page.has_next(),
        'prev_page': page.next_page_number(),
        'next_page': page.previous_page_number(),
        'pages': tads.page_range,
        'page_id': int(page_id),
        'titulo': 'Listado TADs',
        'tipo': 'publish',
    })

def edit(request, tad_id=None):
	try:
		if tad_id:
			tad = TAD.objects.get(pk=tad_id)
		else:
			tad = TAD()
		attrs = []
		if request.method == 'POST':
			form = TADForm(request.POST, instance=tad, auto_id=False)
			attr_name = request.POST.getlist('attr_name')
			attr_tad = request.POST.getlist('attr_tad')
			for i in range(0, len(attr_name)):
				attrs.append([
					attr_name[i],
					int(attr_tad[i])
				])
			if form.is_valid():
				form.save()
				TADAttrs.objects.filter(tad__id=tad_id).delete()
				for i in range(0, len(attr_name)):
					a = TADAttrs()
					a.name = attr_name[i]
					a.tad_type_id = int(attr_tad[i])
					a.tad_id = tad.id
					a.save()
				return redirect('/soap/')
		else:
			form = TADForm(instance=tad, auto_id=False)
			a = TADAttrs.objects.filter(tad__id=tad_id)
			for i in range(0, len(a)):
				attrs.append([
					a[i].name,
					a[i].tad_type_id
				])
	except TAD.DoesNotExist:
		raise Http404

	tads = TAD.objects.exclude(id=tad_id)
	return render_to_response('soap/edit.html', {
		'form': form,
		'attrs': attrs,
		'tad': tad,
		'tads': tads,
		'button': 'modifica' if tad_id else 'crear',
		'forms': [{
			'id': 'tad',
			'name': 'TAD'
		}],
		'titulo': 'Edita TAD' if tad_id else 'Crea TAD',
		'tipo': 'publish',
	}, context_instance=RequestContext(request))

def delete(request, tad_id):
	TAD.objects.get(pk=tad_id).delete()
	return redirect('/soap/')
