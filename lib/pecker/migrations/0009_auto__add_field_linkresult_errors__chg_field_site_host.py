# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'LinkResult.errors'
        db.add_column('pecker_linkresult', 'errors',
                      self.gf('django.db.models.fields.TextField')(default=None, null=True, blank=True),
                      keep_default=False)


        # Changing field 'Site.host'
        db.alter_column('pecker_site', 'host', self.gf('django.db.models.fields.CharField')(max_length=30, null=True))

    def backwards(self, orm):
        # Deleting field 'LinkResult.errors'
        db.delete_column('pecker_linkresult', 'errors')


        # Changing field 'Site.host'
        db.alter_column('pecker_site', 'host', self.gf('django.db.models.fields.CharField')(max_length=15, null=True))

    models = {
        'pecker.case': {
            'Meta': {'object_name': 'Case'},
            'form_index': ('django.db.models.fields.IntegerField', [], {}),
            'form_params': ('json_field.fields.JSONField', [], {'default': "u'null'", 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'link': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['pecker.Link']"}),
            'query_params': ('json_field.fields.JSONField', [], {'default': "u'null'", 'null': 'True', 'blank': 'True'})
        },
        'pecker.link': {
            'Meta': {'object_name': 'Link'},
            'available': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'site': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['pecker.Site']"}),
            'url': ('django.db.models.fields.CharField', [], {'max_length': '300'}),
            'url_hash': ('django.db.models.fields.CharField', [], {'db_index': 'True', 'unique': 'True', 'max_length': '50', 'blank': 'True'})
        },
        'pecker.linkresult': {
            'Meta': {'object_name': 'LinkResult'},
            'case': ('django.db.models.fields.related.ForeignKey', [], {'default': 'None', 'to': "orm['pecker.Case']", 'null': 'True', 'blank': 'True'}),
            'content_type': ('django.db.models.fields.CharField', [], {'max_length': '20', 'null': 'True', 'blank': 'True'}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'errors': ('django.db.models.fields.TextField', [], {'default': 'None', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'link': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['pecker.Link']"}),
            'output': ('django.db.models.fields.TextField', [], {'default': 'None', 'null': 'True', 'blank': 'True'}),
            'run': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['pecker.Run']"}),
            'status': ('django.db.models.fields.CharField', [], {'max_length': '3', 'null': 'True', 'blank': 'True'})
        },
        'pecker.run': {
            'Meta': {'object_name': 'Run'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '20'}),
            'site': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['pecker.Site']"})
        },
        'pecker.site': {
            'Meta': {'object_name': 'Site'},
            'host': ('django.db.models.fields.CharField', [], {'max_length': '30', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '20'}),
            'scheme': ('django.db.models.fields.CharField', [], {'default': "'https'", 'max_length': '5'}),
            'start_url': ('django.db.models.fields.CharField', [], {'max_length': '300', 'null': 'True', 'blank': 'True'})
        }
    }

    complete_apps = ['pecker']