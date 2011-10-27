# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'Groups'
        db.create_table('phas_groups', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('group', self.gf('django.db.models.fields.CharField')(max_length=50)),
        ))
        db.send_create_signal('phas', ['Groups'])

        # Adding model 'Phas'
        db.create_table('phas_phas', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('module', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('group', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['phas.Groups'])),
            ('code', self.gf('django.db.models.fields.TextField')()),
            ('version', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('created_at', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2011, 10, 26, 23, 38, 10, 103687), blank=True)),
        ))
        db.send_create_signal('phas', ['Phas'])

        # Adding model 'Databases'
        db.create_table('phas_databases', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=50, unique=True)),
            ('DSN', self.gf('django.db.models.fields.CharField')(max_length=256)),
            ('USR', self.gf('django.db.models.fields.CharField')(max_length=50, null=True, blank=True)),
            ('PWD', self.gf('django.db.models.fields.CharField')(max_length=50, null=True, blank=True)),
        ))
        db.send_create_signal('phas', ['Databases'])


    def backwards(self, orm):
        
        # Deleting model 'Groups'
        db.delete_table('phas_groups')

        # Deleting model 'Phas'
        db.delete_table('phas_phas')

        # Deleting model 'Databases'
        db.delete_table('phas_databases')


    models = {
        'phas.databases': {
            'DSN': ('django.db.models.fields.CharField', [], {'max_length': '256'}),
            'Meta': {'object_name': 'Databases'},
            'PWD': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'USR': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50', 'unique': 'True'})
        },
        'phas.groups': {
            'Meta': {'object_name': 'Groups'},
            'group': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        'phas.phas': {
            'Meta': {'object_name': 'Phas'},
            'code': ('django.db.models.fields.TextField', [], {}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2011, 10, 26, 23, 38, 10, 103687)', 'blank': 'True'}),
            'group': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['phas.Groups']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'module': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'version': ('django.db.models.fields.IntegerField', [], {'default': '0'})
        }
    }

    complete_apps = ['phas']
