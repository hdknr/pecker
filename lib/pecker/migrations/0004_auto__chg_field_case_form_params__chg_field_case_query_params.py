# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):

        # Changing field 'Case.form_params'
        db.alter_column(u'pecker_case', 'form_params', self.gf('json_field.fields.JSONField')(null=True))

        # Changing field 'Case.query_params'
        db.alter_column(u'pecker_case', 'query_params', self.gf('json_field.fields.JSONField')(null=True))

    def backwards(self, orm):

        # Changing field 'Case.form_params'
        db.alter_column(u'pecker_case', 'form_params', self.gf('json_field.fields.JSONField')())

        # Changing field 'Case.query_params'
        db.alter_column(u'pecker_case', 'query_params', self.gf('json_field.fields.JSONField')())

    models = {
        u'pecker.case': {
            'Meta': {'object_name': 'Case'},
            'form_index': ('django.db.models.fields.IntegerField', [], {}),
            'form_params': ('json_field.fields.JSONField', [], {'default': "u'null'", 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'link': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['pecker.Link']"}),
            'query_params': ('json_field.fields.JSONField', [], {'default': "u'null'", 'null': 'True', 'blank': 'True'})
        },
        u'pecker.link': {
            'Meta': {'object_name': 'Link'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'site': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['pecker.Site']"}),
            'url': ('django.db.models.fields.CharField', [], {'max_length': '300'}),
            'url_hash': ('django.db.models.fields.CharField', [], {'db_index': 'True', 'unique': 'True', 'max_length': '50', 'blank': 'True'})
        },
        u'pecker.linkresult': {
            'Meta': {'object_name': 'LinkResult'},
            'case': ('django.db.models.fields.related.ForeignKey', [], {'default': 'None', 'to': u"orm['pecker.Case']", 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'link': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['pecker.Link']"}),
            'output': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'run': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['pecker.Run']"}),
            'status': ('django.db.models.fields.CharField', [], {'max_length': '3', 'null': 'True', 'blank': 'True'})
        },
        u'pecker.run': {
            'Meta': {'object_name': 'Run'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '20'}),
            'site': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['pecker.Site']"})
        },
        u'pecker.site': {
            'Meta': {'object_name': 'Site'},
            'host': ('django.db.models.fields.CharField', [], {'max_length': '15', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '20'}),
            'start_url': ('django.db.models.fields.CharField', [], {'max_length': '300', 'null': 'True', 'blank': 'True'})
        }
    }

    complete_apps = ['pecker']