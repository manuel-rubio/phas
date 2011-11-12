# -*- coding: utf-8 -*-
from django.shortcuts import render_to_response, redirect
from django.http import Http404
from phas.models import *
from phas.forms import *
from django.template import RequestContext
from django.core.paginator import Paginator, InvalidPage
from datetime import *
from difflib import *

def diff(request, code_id, src="0", dst="1"):
	code = Phas.objects.get(pk=code_id)
	codes = Phas.objects.filter(module=code.module, group__id=code.group_id)
	# TODO: cambiar esto por versiones a elegir
	code1 = codes[int(src)].code.splitlines(1)
	code2 = codes[int(dst)].code.splitlines(1)
	diff = HtmlDiff()
	diffs = diff.make_table(
		code1, code2, 
		codes[int(src)].module + "@" + str(codes[int(src)].version),
		codes[int(dst)].module + "@" + str(codes[int(dst)].version))
	return render_to_response('codes/diff.html',{
	    'titulo': 'Diferencias',
	    'tipo': 'javascript',
		'table_diff': diffs,
		'total_diff': len(codes)-1,
		'total_diff_list': range(0, len(codes)),
		'src': int(src),
		'dst': int(dst),
		'code_id': int(code_id),
	})

def index(request, page_id = 1):
    page = int(page_id)
    data = {}
    raw = []
    group_id = 0
    if 'group' in request.REQUEST and request.REQUEST['group'] != '':
        raw = Phas.objects.filter(group__id=request.REQUEST['group'])
        group_id = request.REQUEST['group']
    else:
        raw = Phas.objects.all()
    for p in raw:
        i = str(p.group_id) + '/' + p.module
        if i not in data:
            data[i] = p
        else:
            if data[i].version < p.version:
                data[i] = p

    cod = []
    for k,v in data.iteritems():
        cod.append(v)

    for i in xrange(0,len(cod)-1):
        k = i
        for j in xrange(i+1, len(cod)):
            if cod[j].id > cod[k].id:
                k = j
        if k != i:
            cod[i], cod[k] = cod[k], cod[i]

    codes = Paginator(cod, 5)
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
        'tipo': 'javascript',
		'group_id': int(group_id),
		'grupos': Groups.objects.all(),
		'filtro': True,
    })

def edit(request, code_id=None):
    try:
        if code_id:
            code = Phas.objects.get(pk=code_id)
        else:
            code = Phas()
            code.version = 1
        if request.method == 'POST':
            if code_id:
                form = PhasFormEdit(request.POST, instance=code, auto_id=False)
            else:
                form = PhasForm(request.POST, instance=code, auto_id=False)
            if form.is_valid():
                if code_id:
                    code.version += 1
                    code.created_at = datetime.now()
                    code.id = None
                form.save()
                return redirect('/code/')
        else:
            if code_id:
                form = PhasFormEdit(instance=code, auto_id=False)
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
        'tipo': 'javascript',
    }, context_instance=RequestContext(request))

def delete(request, code_id):
    code = Phas.objects.get(pk=code_id)
    Phas.objects.filter(module=code.module).filter(group__id=code.group_id).delete()
    return redirect('/code/')
