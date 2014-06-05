# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting field 'Message.template_type'
        db.delete_column('mail_message', 'template_type')

        # Adding field 'Message.template'
        db.add_column('mail_message', 'template',
                      self.gf('django.db.models.fields.related.ForeignKey')(to=orm['mail.MailTemplate'], blank=True, null=True),
                      keep_default=False)

        # Adding field 'MailTemplate.template_name'
        db.add_column('mail_mailtemplate', 'template_name',
                      self.gf('django.db.models.fields.CharField')(max_length=100, default='', blank=True),
                      keep_default=False)


    def backwards(self, orm):
        # Adding field 'Message.template_type'
        db.add_column('mail_message', 'template_type',
                      self.gf('django.db.models.fields.CharField')(max_length=32, default='django'),
                      keep_default=False)

        # Deleting field 'Message.template'
        db.delete_column('mail_message', 'template_id')

        # Deleting field 'MailTemplate.template_name'
        db.delete_column('mail_mailtemplate', 'template_name')


    models = {
        'contenttypes.contenttype': {
            'Meta': {'db_table': "'django_content_type'", 'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType'},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'mail.mail': {
            'Meta': {'object_name': 'Mail', 'ordering': "['created']"},
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'message': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['mail.Message']"}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'blank': 'True', 'auto_now': 'True'}),
            'retry_count': ('django.db.models.fields.IntegerField', [], {'blank': 'True', 'null': 'True'}),
            'sent': ('django.db.models.fields.DateTimeField', [], {'blank': 'True', 'null': 'True'}),
            'sent_response_code': ('django.db.models.fields.CharField', [], {'max_length': '256', 'blank': 'True', 'null': 'True'})
        },
        'mail.mailfield': {
            'Meta': {'object_name': 'MailField'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'key': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'mail': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['mail.Mail']"}),
            'value': ('django.db.models.fields.CharField', [], {'max_length': '256'})
        },
        'mail.mailtemplate': {
            'Meta': {'object_name': 'MailTemplate', 'ordering': "('title',)"},
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'help_text': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_html': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'blank': 'True', 'auto_now': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '50'}),
            'subject': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'template_name': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'template_type': ('django.db.models.fields.CharField', [], {'max_length': '32', 'default': "'django'"}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'mail.message': {
            'Meta': {'object_name': 'Message', 'ordering': "['-created']", 'unique_together': "(('object_id', 'content_type'),)"},
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_html': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'blank': 'True', 'auto_now': 'True'}),
            'object_id': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'subject': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'template': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['mail.MailTemplate']", 'blank': 'True', 'null': 'True'})
        }
    }

    complete_apps = ['mail']