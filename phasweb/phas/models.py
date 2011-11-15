# -*- coding: utf-8 -*-
from django.db import models
import datetime

class Modules(models.Model):
    name = models.CharField(max_length=50)

    def __unicode__(self):
        return self.name

class Codes(models.Model):
    name = models.CharField(max_length=50)
    module = models.ForeignKey('Modules')
    version = models.IntegerField(default=1)
    doc = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, blank=True)

    def __unicode__(self):
        return self.name

class CodeVersions(models.Model):
    content = models.TextField()
    version = models.IntegerField(default=1)
    return_attr = models.ForeignKey('TAD', blank=True, null=True)
    code = models.ForeignKey('Codes')

    def __unicode__(self):
        return str(self.code.name) + "@" + str(self.version)

    class Meta:
        ordering = ('version',)

class CodeAttrs(models.Model):
    name = models.CharField(max_length=50)
    tad = models.ForeignKey('TAD')
    code = models.ForeignKey('CodeVersions')

    def __unicode__(self):
        return self.tad + " " + self.name

class TAD(models.Model):
    name = models.CharField(max_length=50)
    xsd_name = models.CharField(max_length=50)
    TYPE_CHOICES = (
        ( 'C', 'Complejo' ),
        ( 'A', 'Array' ),
    )
    tad_type = models.CharField(max_length=1, default='S', choices=TYPE_CHOICES)

    def __unicode__(self):
        return self.name

class TADAttrs(models.Model):
    name = models.CharField(max_length=50)
    tad = models.ForeignKey('TAD')
    tad_type = models.ForeignKey('TAD', related_name='+')
    min_occurs = models.IntegerField(default=0)
    max_occurs = models.IntegerField(default=1)

    def __unicode__(self):
        return self.name

class Databases(models.Model):
    name = models.CharField(max_length=50, unique=True)
    DSN = models.CharField(max_length=256)
    USR = models.CharField(max_length=50, null=True, blank=True)
    PWD = models.CharField(max_length=50, null=True, blank=True)

    def __unicode__(self):
        return self.name
