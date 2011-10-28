# -*- coding: utf-8 -*-
from django import forms
from phas.models import *

class DatabasesForm(forms.ModelForm):
    name = forms.CharField(label='Nombre')
    USR = forms.CharField(label='Usuario', required=False)
    PWD = forms.CharField(label='Clave', required=False)
    class Meta:
        model = Databases

class GroupsForm(forms.ModelForm):
    group = forms.CharField(label='Nombre de Grupo', required=True)
    class Meta:
        model = Groups

class PhasForm(forms.ModelForm):
    class Meta:
        model = Phas

