# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Site'
        db.create_table(u'pecker_site', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(unique=True, max_length=20)),
            ('host', self.gf('django.db.models.fields.CharField')(max_length=15, null=True, blank=True)),
            ('auth_url', self.gf('django.db.models.fields.CharField')(max_length=150, null=True, blank=True)),
            ('auth_user', self.gf('django.db.models.fields.CharField')(max_length=15, null=True, blank=True)),
            ('auth_password', self.gf('django.db.models.fields.CharField')(max_length=15, null=True, blank=True)),
        ))
        db.send_create_signal(u'pecker', ['Site'])

        # Adding model 'Run'
        db.create_table(u'pecker_run', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('site', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['pecker.Site'])),
            ('name', self.gf('django.db.models.fields.CharField')(unique=True, max_length=20)),
        ))
        db.send_create_signal(u'pecker', ['Run'])

        # Adding model 'Link'
        db.create_table(u'pecker_link', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('site', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['pecker.Site'])),
            ('url_hash', self.gf('django.db.models.fields.CharField')(unique=True, max_length=50, db_index=True)),
            ('url', self.gf('django.db.models.fields.CharField')(max_length=300)),
        ))
        db.send_create_signal(u'pecker', ['Link'])

        # Adding model 'Case'
        db.create_table(u'pecker_case', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('link', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['pecker.Link'])),
            ('form_index', self.gf('django.db.models.fields.IntegerField')()),
            ('form_params', self.gf('json_field.fields.JSONField')(default=u'null')),
        ))
        db.send_create_signal(u'pecker', ['Case'])

        # Adding model 'LinkResult'
        db.create_table(u'pecker_linkresult', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('run', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['pecker.Run'])),
            ('link', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['pecker.Link'])),
            ('status', self.gf('django.db.models.fields.CharField')(max_length=3, null=True, blank=True)),
            ('output', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
        ))
        db.send_create_signal(u'pecker', ['LinkResult'])


    def backwards(self, orm):
        # Deleting model 'Site'
        db.delete_table(u'pecker_site')

        # Deleting model 'Run'
        db.delete_table(u'pecker_run')

        # Deleting model 'Link'
        db.delete_table(u'pecker_link')

        # Deleting model 'Case'
        db.delete_table(u'pecker_case')

        # Deleting model 'LinkResult'
        db.delete_table(u'pecker_linkresult')


    models = {
        u'pecker.case': {
            'Meta': {'object_name': 'Case'},
            'form_index': ('django.db.models.fields.IntegerField', [], {}),
            'form_params': ('json_field.fields.JSONField', [], {'default': "u'null'"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'link': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['pecker.Link']"})
        },
        u'pecker.link': {
            'Meta': {'object_name': 'Link'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'site': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['pecker.Site']"}),
            'url': ('django.db.models.fields.CharField', [], {'max_length': '300'}),
            'url_hash': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '50', 'db_index': 'True'})
        },
        u'pecker.linkresult': {
            'Meta': {'object_name': 'LinkResult'},
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
            'auth_password': ('django.db.models.fields.CharField', [], {'max_length': '15', 'null': 'True', 'blank': 'True'}),
            'auth_url': ('django.db.models.fields.CharField', [], {'max_length': '150', 'null': 'True', 'blank': 'True'}),
            'auth_user': ('django.db.models.fields.CharField', [], {'max_length': '15', 'null': 'True', 'blank': 'True'}),
            'host': ('django.db.models.fields.CharField', [], {'max_length': '15', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '20'})
        }
    }

    complete_apps = ['pecker']