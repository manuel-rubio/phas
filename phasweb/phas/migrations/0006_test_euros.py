# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import DataMigration
from django.db import models
from phas.models import *

class Migration(DataMigration):

    def forwards(self, orm):
        try:
            module = Modules.objects.get(name='test')
        except Modules.DoesNotExist:
            module = Modules()
            module.name = 'test'
            module.save()

        code = Codes()
        code.name = 'euros'
        code.module_id = module.id
        code.version = 1
        code.save()

        code_ver = CodeVersions()
        code_ver.content = """
var spider = new DataAccess('euros');
var monedas = spider.dql('SELECT * FROM monedas');

var url = 'http://www.webservicex.net/CurrencyConvertor.asmx?WSDL';
var api = new SoapCli(url);
var convs = new Object();

for (var i in monedas) {
    var conversion;
    var moneda = monedas[i].moneda;
    convs[moneda] = new Object();

    logger.log("Moneda: " + moneda, PEAR_LOG_DEBUG);
    ConversionRate = {
        FromCurrency : moneda,
        ToCurrency: "EUR"
    }

    conversion = api.call("ConversionRate", [ConversionRate]);
    logger.log('resultado: ' + conversion.ConversionRateResult, PEAR_LOG_INFO);
    convs[moneda]['a_euros'] = conversion.ConversionRateResult;

    ConversionRate = {
        FromCurrency : "EUR",
        ToCurrency: moneda
    }

    conversion = api.call("ConversionRate", [ConversionRate]);
    logger.log('resultado: ' + conversion.ConversionRateResult, PEAR_LOG_INFO);
    convs[moneda]['desde_euros'] = conversion.ConversionRateResult;

    spider.dml('DELETE FROM valor_euro WHERE moneda = ?', [[ moneda ]] );
    spider.dml('INSERT INTO valor_euro (moneda, a_euros, desde_euros) VALUES (?, ?, ?)',
               [[ moneda, convs[moneda]['a_euros'], convs[moneda]['desde_euros'] ]] );

}

logger.log('resultado: ' + convs.toSource());
logger.log('finalizado.', PEAR_LOG_INFO);

convs;
        """
        code_ver.version = 1
        code_ver.code_id = code.id
        code_ver.save()

        db = Databases()
        db.name = 'euros'
        db.DSN = 'sqlite:/tmp/euros.sqlite'
        db.save()

    def backwards(self, orm):
        CodeVersions.objects.filter(code__name='euros', code__module__name='test').delete()
        Codes.objects.filter(name='euros', module__name='test').delete()
        Databases.objects.filter(name='euros').delete()

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
