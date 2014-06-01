# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'MailField'
        db.create_table('mail_mailfield', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('mail', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['mail.Mail'])),
            ('key', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('value', self.gf('django.db.models.fields.CharField')(max_length=256)),
        ))
        db.send_create_signal('mail', ['MailField'])

        # Adding field 'MailTemplate.is_html'
        db.add_column('mail_mailtemplate', 'is_html',
                      self.gf('django.db.models.fields.BooleanField')(default=False),
                      keep_default=False)

        # Adding field 'Mail.sent_response_code'
        db.add_column('mail_mail', 'sent_response_code',
                      self.gf('django.db.models.fields.CharField')(null=True, max_length=256, blank=True),
                      keep_default=False)

        # Adding field 'Message.is_html'
        db.add_column('mail_message', 'is_html',
                      self.gf('django.db.models.fields.BooleanField')(default=False),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting model 'MailField'
        db.delete_table('mail_mailfield')

        # Deleting field 'MailTemplate.is_html'
        db.delete_column('mail_mailtemplate', 'is_html')

        # Deleting field 'Mail.sent_response_code'
        db.delete_column('mail_mail', 'sent_response_code')

        # Deleting field 'Message.is_html'
        db.delete_column('mail_message', 'is_html')


    models = {
        'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'mail.mail': {
            'Meta': {'ordering': "['created']", 'object_name': 'Mail'},
            'created': ('django.db.models.fields.DateTimeField', [], {'blank': 'True', 'auto_now_add': 'True'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'message': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['mail.Message']"}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'retry_count': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'sent': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'sent_response_code': ('django.db.models.fields.CharField', [], {'null': 'True', 'max_length': '256', 'blank': 'True'})
        },
        'mail.mailfield': {
            'Meta': {'object_name': 'MailField'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'key': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'mail': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['mail.Mail']"}),
            'value': ('django.db.models.fields.CharField', [], {'max_length': '256'})
        },
        'mail.mailtemplate': {
            'Meta': {'ordering': "('title',)", 'object_name': 'MailTemplate'},
            'created': ('django.db.models.fields.DateTimeField', [], {'blank': 'True', 'auto_now_add': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'help_text': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_html': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '50', 'unique': 'True'}),
            'subject': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'mail.message': {
            'Meta': {'ordering': "['-created']", 'unique_together': "(('object_id', 'content_type'),)", 'object_name': 'Message'},
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'created': ('django.db.models.fields.DateTimeField', [], {'blank': 'True', 'auto_now_add': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_html': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'object_id': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'subject': ('django.db.models.fields.CharField', [], {'max_length': '200'})
        }
    }

    complete_apps = ['mail']