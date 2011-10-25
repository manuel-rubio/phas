# -*- coding: utf-8 -*-
from django.shortcuts import render_to_response
from django.http import Http404
from phas.models import *
from django.template import RequestContext

def index(request):
    databases = BasesDeDatos.objects.all()
    return render_to_response('phas/index.html', {
        'databases': databases
    })

def detail(request, database_id):
    try:
        database = BasesDeDatos.objects.get(pk=database_id)
        form = BasesDeDatosForm(instance=database)
    except BasesDeDatos.DoesNotExist:
        raise Http404
    return render_to_response('phas/detail.html', {
        'form': form,
        'database': database
    }, context_instance=RequestContext(request))

def save(request, database_id):
    return detail(request, database_id)
