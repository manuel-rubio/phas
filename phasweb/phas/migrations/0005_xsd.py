# -*- coding: utf-8 -*-

import datetime
from south.db import db
from south.v2 import DataMigration
from django.db import models
from phas.models import *

class Migration(DataMigration):

    def forwards(self, orm):
        data = [
            { 'name': 'string', 'xsd_name': 'xsd:string' },
            { 'name': 'integer', 'xsd_name': 'xsd:integer' },
            { 'name': 'boolean', 'xsd_name': 'xsd:boolean' },
            { 'name': 'boolean', 'xsd_name': 'xsd:boolean' },
            { 'name': 'float', 'xsd_name': 'xsd:float' },
            { 'name': 'double', 'xsd_name': 'xsd:double' },
            { 'name': 'string[]', 'xsd_name': 'tns:ArrayOfString' },
            { 'name': 'string[][]', 'xsd_name': 'tns:MatrixOfString' },
            { 'name': 'duration', 'xsd_name': 'xsd:duration' },
            { 'name': 'dateTime', 'xsd_name': 'xsd:dateTime' },
            { 'name': 'date', 'xsd_name': 'xsd:date' },
            { 'name': 'time', 'xsd_name': 'xsd:time' },
            { 'name': 'hexBinary', 'xsd_name': 'xsd:hexBinary' },
            { 'name': 'base64Binary', 'xsd_name': 'xsd:base64Binary' },
            { 'name': 'anyURI', 'xsd_name': 'xsd:anyURI' },
        ]
        for d in data:
            t = TAD()
            t.name = d['name']
            t.xsd_name = d['xsd_name']
            t.tad_type = 'S'
            t.save()


    def backwards(self, orm):
        TAD.objects.filter(tad_type='S').delete()


    models = {
        'phas.codeattrs': {
            'Meta': {'object_name': 'CodeAttrs'},
            'code': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['phas.CodeVersions']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'tad': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['phas.TAD']"})
        },
        'phas.codes': {
            'Meta': {'object_name': 'Codes'},
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'doc': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'module': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['phas.Modules']"}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'version': ('django.db.models.fields.IntegerField', [], {'default': '1'})
        },
        'phas.codeversions': {
            'Meta': {'ordering': "('version',)", 'object_name': 'CodeVersions'},
            'code': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['phas.Codes']"}),
            'content': ('django.db.models.fields.TextField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'return_attr': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['phas.TAD']", 'null': 'True', 'blank': 'True'}),
            'version': ('django.db.models.fields.IntegerField', [], {'default': '1'})
        },
        'phas.databases': {
            'DSN': ('django.db.models.fields.CharField', [], {'max_length': '256'}),
            'Meta': {'object_name': 'Databases'},
            'PWD': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'USR': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '50'})
        },
        'phas.modules': {
            'Meta': {'object_name': 'Modules'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'phas.tad': {
            'Meta': {'object_name': 'TAD'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'tad_type': ('django.db.models.fields.CharField', [], {'default': "'S'", 'max_length': '1'}),
            'xsd_name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'phas.tadattrs': {
            'Meta': {'object_name': 'TADAttrs'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'max_occurs': ('django.db.models.fields.IntegerField', [], {'default': '1'}),
            'min_occurs': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'tad': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['phas.TAD']"}),
            'tad_type': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'+'", 'to': "orm['phas.TAD']"})
        }
    }

    complete_apps = ['phas']
