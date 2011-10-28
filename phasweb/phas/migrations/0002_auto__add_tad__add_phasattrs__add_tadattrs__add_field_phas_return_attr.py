# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'TAD'
        db.create_table('phas_tad', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('complex', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('xsd_name', self.gf('django.db.models.fields.CharField')(max_length=50)),
        ))
        db.send_create_signal('phas', ['TAD'])

        # Adding model 'PhasAttrs'
        db.create_table('phas_phasattrs', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('tad', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['phas.TAD'], null=True, blank=True)),
            ('code', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['phas.Phas'], null=True, blank=True)),
        ))
        db.send_create_signal('phas', ['PhasAttrs'])

        # Adding model 'TADAttrs'
        db.create_table('phas_tadattrs', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('tad', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['phas.TAD'], null=True, blank=True)),
        ))
        db.send_create_signal('phas', ['TADAttrs'])

        # Adding field 'Phas.return_attr'
        db.add_column('phas_phas', 'return_attr', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['phas.TAD'], null=True, blank=True), keep_default=False)


    def backwards(self, orm):
        
        # Deleting model 'TAD'
        db.delete_table('phas_tad')

        # Deleting model 'PhasAttrs'
        db.delete_table('phas_phasattrs')

        # Deleting model 'TADAttrs'
        db.delete_table('phas_tadattrs')

        # Deleting field 'Phas.return_attr'
        db.delete_column('phas_phas', 'return_attr_id')


    models = {
        'phas.databases': {
            'DSN': ('django.db.models.fields.CharField', [], {'max_length': '256'}),
            'Meta': {'object_name': 'Databases'},
            'PWD': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'USR': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '50'})
        },
        'phas.groups': {
            'Meta': {'object_name': 'Groups'},
            'group': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        'phas.phas': {
            'Meta': {'object_name': 'Phas'},
            'code': ('django.db.models.fields.TextField', [], {}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2011, 10, 28, 18, 57, 48, 431682)', 'blank': 'True'}),
            'group': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['phas.Groups']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'module': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'return_attr': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['phas.TAD']", 'null': 'True', 'blank': 'True'}),
            'version': ('django.db.models.fields.IntegerField', [], {'default': '0'})
        },
        'phas.phasattrs': {
            'Meta': {'object_name': 'PhasAttrs'},
            'code': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['phas.Phas']", 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'tad': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['phas.TAD']", 'null': 'True', 'blank': 'True'})
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
