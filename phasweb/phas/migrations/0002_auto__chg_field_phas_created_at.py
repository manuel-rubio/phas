# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Changing field 'Phas.created_at'
        db.alter_column('phas_phas', 'created_at', self.gf('django.db.models.fields.DateTimeField')())


    def backwards(self, orm):
        
        # Changing field 'Phas.created_at'
        db.alter_column('phas_phas', 'created_at', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, null=True))


    models = {
        'phas.phas': {
            'Meta': {'object_name': 'Phas'},
            'code': ('django.db.models.fields.TextField', [], {}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2011, 10, 23, 2, 22, 59, 808158)', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'module': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'version': ('django.db.models.fields.IntegerField', [], {'default': '0'})
        }
    }

    complete_apps = ['phas']
