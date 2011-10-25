# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Changing field 'BasesDeDatos.PWD'
        db.alter_column('phas_basesdedatos', 'PWD', self.gf('django.db.models.fields.CharField')(max_length=50, null=True))

        # Changing field 'BasesDeDatos.USR'
        db.alter_column('phas_basesdedatos', 'USR', self.gf('django.db.models.fields.CharField')(max_length=50, null=True))


    def backwards(self, orm):
        
        # Changing field 'BasesDeDatos.PWD'
        db.alter_column('phas_basesdedatos', 'PWD', self.gf('django.db.models.fields.CharField')(default='', max_length=50))

        # Changing field 'BasesDeDatos.USR'
        db.alter_column('phas_basesdedatos', 'USR', self.gf('django.db.models.fields.CharField')(default='', max_length=50))


    models = {
        'phas.basesdedatos': {
            'DSN': ('django.db.models.fields.CharField', [], {'max_length': '256'}),
            'Meta': {'object_name': 'BasesDeDatos'},
            'PWD': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True'}),
            'USR': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        'phas.phas': {
            'Meta': {'object_name': 'Phas'},
            'code': ('django.db.models.fields.TextField', [], {}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2011, 10, 25, 1, 27, 43, 156691)', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'module': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'version': ('django.db.models.fields.IntegerField', [], {'default': '0'})
        }
    }

    complete_apps = ['phas']
