# -*- coding: utf-8 -*-
from django import forms
from django.db import models
import datetime

class Groups(models.Model):
    group = models.CharField(max_length=50)

class Phas(models.Model):
    module = models.CharField(max_length=50)
    group = models.ForeignKey('Groups')
    code = models.TextField()
    version = models.IntegerField(default=0)
    # FIXME: datetime.now deberia de ser usado ya que datetime.now() se cambia por la fecha
    # en el momento de la creacion.
    created_at = models.DateTimeField(default=datetime.datetime.now(), blank=True)

class Databases(models.Model):
    name = models.CharField(max_length=50, unique=True)
    DSN = models.CharField(max_length=256)
    USR = models.CharField(max_length=50, null=True, blank=True)
    PWD = models.CharField(max_length=50, null=True, blank=True)

    def __unicode__(self):
        return self.name

class DatabasesForm(forms.ModelForm):
    name = forms.CharField(label='Nombre')
    USR = forms.CharField(label='Usuario')
    PWD = forms.CharField(label='Clave')
    class Meta:
        model = Databases

class PhasForm(forms.ModelForm):
    class Meta:
        model = Phas

