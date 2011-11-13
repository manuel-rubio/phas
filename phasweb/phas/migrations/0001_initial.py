# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'Modules'
        db.create_table('phas_modules', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=50)),
        ))
        db.send_create_signal('phas', ['Modules'])

        # Adding model 'Codes'
        db.create_table('phas_codes', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('module', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['phas.Modules'])),
            ('version', self.gf('django.db.models.fields.IntegerField')(default=1)),
            ('created_at', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('updated_at', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
        ))
        db.send_create_signal('phas', ['Codes'])

        # Adding model 'CodeVersions'
        db.create_table('phas_codeversions', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('content', self.gf('django.db.models.fields.TextField')()),
            ('version', self.gf('django.db.models.fields.IntegerField')(default=1)),
            ('return_attr', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['phas.TAD'], null=True, blank=True)),
            ('code', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['phas.Codes'])),
        ))
        db.send_create_signal('phas', ['CodeVersions'])

        # Adding model 'CodeAttrs'
        db.create_table('phas_codeattrs', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('tad', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['phas.TAD'], null=True, blank=True)),
            ('code', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['phas.CodeVersions'], null=True, blank=True)),
        ))
        db.send_create_signal('phas', ['CodeAttrs'])

        # Adding model 'TAD'
        db.create_table('phas_tad', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('complex', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('xsd_name', self.gf('django.db.models.fields.CharField')(max_length=50)),
        ))
        db.send_create_signal('phas', ['TAD'])

        # Adding model 'TADAttrs'
        db.create_table('phas_tadattrs', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('tad', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['phas.TAD'], null=True, blank=True)),
        ))
        db.send_create_signal('phas', ['TADAttrs'])

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
        
        # Deleting model 'Modules'
        db.delete_table('phas_modules')

        # Deleting model 'Codes'
        db.delete_table('phas_codes')

        # Deleting model 'CodeVersions'
        db.delete_table('phas_codeversions')

        # Deleting model 'CodeAttrs'
        db.delete_table('phas_codeattrs')

        # Deleting model 'TAD'
        db.delete_table('phas_tad')

        # Deleting model 'TADAttrs'
        db.delete_table('phas_tadattrs')

        # Deleting model 'Databases'
        db.delete_table('phas_databases')


    models = {
        'phas.codeattrs': {
            'Meta': {'object_name': 'CodeAttrs'},
            'code': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['phas.CodeVersions']", 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'tad': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['phas.TAD']", 'null': 'True', 'blank': 'True'})
        },
        'phas.codes': {
            'Meta': {'object_name': 'Codes'},
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'module': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['phas.Modules']"}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'version': ('django.db.models.fields.IntegerField', [], {'default': '1'})
        },
        'phas.codeversions': {
            'Meta': {'object_name': 'CodeVersions'},
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
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50', 'unique': 'True'})
        },
        'phas.modules': {
            'Meta': {'object_name': 'Modules'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'phas.tad': {
            'Meta': {'object_name': 'TAD'},
            'complex': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'xsd_name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'phas.tadattrs': {
            'Meta': {'object_name': 'TADAttrs'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'tad': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['phas.TAD']", 'null': 'True', 'blank': 'True'})
        }
    }

    complete_apps = ['phas']
