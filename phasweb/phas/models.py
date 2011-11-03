# -*- coding: utf-8 -*-
from django.db import models
import datetime

class Groups(models.Model):
    name = models.CharField(max_length=50)

    def __unicode__(self):
        return self.name

class Phas(models.Model):
    module = models.CharField(max_length=50)
    group = models.ForeignKey('Groups')
    code = models.TextField()
    version = models.IntegerField(default=0)
    # FIXME: datetime.now deberia de ser usado ya que datetime.now() se cambia por la fecha
    # en el momento de la creacion.
    created_at = models.DateTimeField(default=datetime.datetime.now(), blank=True)
    return_attr = models.ForeignKey('TAD', blank=True, null=True)

    def __unicode__(self):
        return self.module

class PhasAttrs(models.Model):
    name = models.CharField(max_length=50)
    tad = models.ForeignKey('TAD', blank=True, null=True)
    code = models.ForeignKey('Phas', blank=True, null=True)

    def __unicode__(self):
        return self.type + ("[]" * self.dim) + " " + self.name

class TAD(models.Model):
    name = models.CharField(max_length=50)
    complex = models.BooleanField(default=False)
    xsd_name = models.CharField(max_length=50)

    def __unicode__(self):
        return self.name

class TADAttrs(models.Model):
    name = models.CharField(max_length=50)
    tad = models.ForeignKey('TAD', blank=True, null=True)
    tad  = models.ForeignKey('TAD', blank=True, null=True)

    def __unicode__(self):
        return self.name

class Databases(models.Model):
    name = models.CharField(max_length=50, unique=True)
    DSN = models.CharField(max_length=256)
    USR = models.CharField(max_length=50, null=True, blank=True)
    PWD = models.CharField(max_length=50, null=True, blank=True)

    def __unicode__(self):
        return self.name

