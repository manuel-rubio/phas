# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Changing field 'CodeAttrs.tad'
        db.alter_column('phas_codeattrs', 'tad_id', self.gf('django.db.models.fields.related.ForeignKey')(default=0, to=orm['phas.TAD']))

        # Changing field 'CodeAttrs.code'
        db.alter_column('phas_codeattrs', 'code_id', self.gf('django.db.models.fields.related.ForeignKey')(default=0, to=orm['phas.CodeVersions']))

        # Adding field 'TADAttrs.tad_type'
        db.add_column('phas_tadattrs', 'tad_type', self.gf('django.db.models.fields.related.ForeignKey')(default=0, related_name='+', to=orm['phas.TAD']), keep_default=False)

        # Changing field 'TADAttrs.tad'
        db.alter_column('phas_tadattrs', 'tad_id', self.gf('django.db.models.fields.related.ForeignKey')(default=0, to=orm['phas.TAD']))


    def backwards(self, orm):
        
        # Changing field 'CodeAttrs.tad'
        db.alter_column('phas_codeattrs', 'tad_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['phas.TAD'], null=True))

        # Changing field 'CodeAttrs.code'
        db.alter_column('phas_codeattrs', 'code_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['phas.CodeVersions'], null=True))

        # Deleting field 'TADAttrs.tad_type'
        db.delete_column('phas_tadattrs', 'tad_type_id')

        # Changing field 'TADAttrs.tad'
        db.alter_column('phas_tadattrs', 'tad_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['phas.TAD'], null=True))


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
            'tad': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['phas.TAD']"}),
            'tad_type': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'+'", 'to': "orm['phas.TAD']"})
        }
    }

    complete_apps = ['phas']
