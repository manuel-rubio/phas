# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'BasesDeDatos'
        db.create_table('phas_basesdedatos', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('DSN', self.gf('django.db.models.fields.CharField')(max_length=256)),
            ('USR', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('PWD', self.gf('django.db.models.fields.CharField')(max_length=50)),
        ))
        db.send_create_signal('phas', ['BasesDeDatos'])


    def backwards(self, orm):
        
        # Deleting model 'BasesDeDatos'
        db.delete_table('phas_basesdedatos')


    models = {
        'phas.basesdedatos': {
            'DSN': ('django.db.models.fields.CharField', [], {'max_length': '256'}),
            'Meta': {'object_name': 'BasesDeDatos'},
            'PWD': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'USR': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        'phas.phas': {
            'Meta': {'object_name': 'Phas'},
            'code': ('django.db.models.fields.TextField', [], {}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2011, 10, 25, 1, 17, 2, 896336)', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'module': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'version': ('django.db.models.fields.IntegerField', [], {'default': '0'})
        }
    }

    complete_apps = ['phas']
