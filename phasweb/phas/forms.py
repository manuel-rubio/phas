# -*- coding: utf-8 -*-
from django import forms
from phas.models import *

class DatabasesForm(forms.ModelForm):
    name = forms.CharField(label='Nombre')
    USR = forms.CharField(label='Usuario', required=False)
    PWD = forms.CharField(label='Clave', required=False)
    DSN = forms.CharField(label='DSN', 
        widget=forms.TextInput(attrs={'size':'100'})
    )
    class Meta:
        model = Databases

class ModulesForm(forms.ModelForm):
    name = forms.CharField(label='Nombre del Módulo', required=True)
    class Meta:
        model = Modules

class CodesForm(forms.ModelForm):
    name = forms.CharField(label='Nombe', required=True)
    module = forms.ModelChoiceField(label='Módulo', required=True, queryset=Modules.objects.all())
    doc = forms.CharField(label='Documentación (WSDL)', required=False,
        widget=forms.Textarea(attrs={'rows':'3', 'cols':'80'})
    )
    class Meta:
        model = Codes
        exclude = ( 'created_at', 'updated_at', 'version' )

class CodeVersionsForm(forms.ModelForm):
    content = forms.CharField(label='Código', required=True,
        widget=forms.Textarea(attrs={'rows':'20', 'cols':'80', 'id': 'mycode_textarea'})
    )
    version = forms.IntegerField(label='Versión',
        widget=forms.TextInput(attrs={'readonly':'true'})
    )
    return_attr = forms.ModelChoiceField(label='Retorno (SOAP)', 
        required=False, queryset=TAD.objects.all()
    )
    class Meta:
        model = CodeVersions
        exclude = ( 'code', )

class TADForm(forms.ModelForm):
	name = forms.CharField(label='Nombre', required=True)
	xsd_name = forms.CharField(label='Nombre XML', required=True)
	tad_type = forms.ChoiceField(label='Tipo de Dato', required=True,
		choices=TAD.TYPE_CHOICES
	)
	class Meta:
		model = TAD
