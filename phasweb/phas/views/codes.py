# -*- coding: utf-8 -*-
from django.shortcuts import render_to_response, redirect
from django.http import Http404
from phas.models import *
from phas.forms import *
from django.template import RequestContext
from django.core.paginator import Paginator, InvalidPage
from datetime import *
from difflib import *

def publish(request, code_id):
    try:
        code = Codes.objects.get(pk=code_id)
        codever = CodeVersions.objects.filter(version=code.version, code__id=code_id)[0]
        attrs = []
        if request.method == 'POST':
            form = CodesSOAPForm(request.POST, instance=code, auto_id=False)
            formVer = CodeVersionsSOAPForm(request.POST, instance=codever, auto_id=False)
            attr_name = request.POST.getlist('attr_name')
            attr_tad = request.POST.getlist('attr_tad')
            for i in range(0, len(attr_name)):
                attrs.append([
                    attr_name[i],
                    int(attr_tad[i])
                ])
            if form.is_valid() and formVer.is_valid():
                form.save()
                formVer.save()
                CodeAttrs.objects.filter(code__id=code_id).delete()
                for i in range(0, len(attr_name)):
                    a = CodeAttrs()
                    a.name = attr_name[i]
                    a.tad_id = int(attr_tad[i])
                    a.code_id = code.id
                    a.save()
                return redirect('/code/')
        else:
            form = CodesSOAPForm(instance=code, auto_id=False)
            formVer = CodeVersionsSOAPForm(instance=codever, auto_id=False)
            a = CodeAttrs.objects.filter(code__id=code_id)
            for i in range(0, len(a)):
                attrs.append([
                    a[i].name,
                    a[i].tad_id
                ])
    except Codes.DoesNotExist:
        raise Http404

    tads = TAD.objects.all()
    return render_to_response('codes/publish.html', {
        'form': form,
        'formVer': formVer,
        'attrs': attrs,
        'tads': tads,
        'code': code,
        'codever': codever,
        'button': 'modifica',
        'forms': [{
            'id': 'code',
            'name': 'Publicación'
        }],
        'titulo': 'Publica el Código',
        'tipo': 'publish',
    }, context_instance=RequestContext(request))

def diff(request, code_id, src="0", dst="1"):
    code = Codes.objects.get(pk=code_id)
    codes = CodeVersions.objects.filter(code__id=code_id)
    code1 = codes[int(src)].content.splitlines(1)
    code2 = codes[int(dst)].content.splitlines(1)
    diff = HtmlDiff()
    diffs = diff.make_table(
        code1, code2,
        codes[int(src)],
        codes[int(dst)])
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
    module_id = 0
    if 'module' in request.REQUEST and request.REQUEST['module'] != '':
        cod = Codes.objects.filter(module__id=request.REQUEST['module'])
        module_id = request.REQUEST['module']
    else:
        cod = Codes.objects.all()

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
        'module_id': int(module_id),
        'modulos': Modules.objects.all(),
        'filtro': True,
    })

def edit(request, code_id=None):
    try:
        if code_id:
            code = Codes.objects.get(pk=code_id)
            codever = CodeVersions.objects.filter(version=code.version, code__id=code_id)[0]
        else:
            code = Codes()
            code.version = 1
            codever = CodeVersions()
            codever.version = 1
        if request.method == 'POST':
            form = CodesForm(request.POST, instance=code, auto_id=False)
            formVer = CodeVersionsForm(request.POST, instance=codever, auto_id=False)
            if form.is_valid() and formVer.is_valid():
                if code_id:
                    code.version += 1
                    codever.version += 1
                    codever.id = None
                form.save()
                codever.code_id = code.id
                formVer.save()
                return redirect('/code/')
        else:
            form = CodesForm(instance=code, auto_id=False)
            formVer = CodeVersionsForm(instance=codever, auto_id=False)
    except Codes.DoesNotExist:
        raise Http404

    return render_to_response('codes/edit.html', {
        'form': form,
        'formVer': formVer,
        'code': code,
        'codever': codever,
        'button': 'modifica' if code_id else 'crear',
        'forms': [{
            'id': 'code',
            'name': 'Código'
        }],
        'titulo': 'Edita Código' if code_id else 'Crea Código',
        'tipo': 'javascript',
    }, context_instance=RequestContext(request))

def delete(request, code_id):
    CodeVersions.objects.filter(code__id=code_id).delete()
    Codes.objects.get(pk=code_id).delete()
    return redirect('/code/')
