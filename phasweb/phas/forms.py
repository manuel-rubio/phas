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

class GroupsForm(forms.ModelForm):
    name = forms.CharField(label='Nombre de Grupo', required=True)
    class Meta:
        model = Groups

class PhasFormEdit(forms.ModelForm):
	code = forms.CharField(label='Código', required=True,
		widget=forms.Textarea(attrs={'rows':'20', 'cols':'80'})
	)
	version = forms.IntegerField(label='Versión',
		widget=forms.TextInput(attrs={'readonly':'true'})
	)
	return_attr = forms.ModelChoiceField(label='Retorno (SOAP)', 
		required=False, queryset=TAD.objects.all()
	)
	class Meta:
		model = Phas
		exclude = ( 'created_at', 'module', 'group' )

class PhasForm(forms.ModelForm):
	module = forms.CharField(label='Nombe del Módulo', required=True)
	group = forms.ModelChoiceField(label='Grupo', required=True, queryset=Groups.objects.all())
	code = forms.CharField(label='Código', required=True,
		widget=forms.Textarea(attrs={'rows':'20', 'cols':'80'})
	)
	version = forms.IntegerField(label='Versión',
		widget=forms.TextInput(attrs={'readonly':'true'})
	)
	return_attr = forms.ModelChoiceField(label='Retorno (SOAP)', 
		required=False, queryset=TAD.objects.all()
	)
	class Meta:
		model = Phas
		exclude = ( 'created_at' )

