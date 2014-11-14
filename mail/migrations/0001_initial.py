# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('contenttypes', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Mail',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', serialize=False, primary_key=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('email', models.EmailField(max_length=75, blank=True)),
                ('retry_count', models.IntegerField(null=True, blank=True)),
                ('sent', models.DateTimeField(null=True, blank=True)),
                ('sent_response_code', models.CharField(null=True, max_length=256, blank=True)),
            ],
            options={
                'ordering': ['created'],
                'verbose_name': 'Mail detail',
                'verbose_name_plural': 'Mail detail',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='MailField',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', serialize=False, primary_key=True)),
                ('key', models.CharField(max_length=100)),
                ('value', models.CharField(max_length=256)),
                ('mail', models.ForeignKey(to='mail.Mail')),
            ],
            options={
                'verbose_name': 'Mail field',
                'verbose_name_plural': 'Mail fields',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='MailTemplate',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', serialize=False, primary_key=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('slug', models.SlugField(unique=True)),
                ('title', models.CharField(max_length=100)),
                ('help_text', models.TextField(blank=True)),
                ('is_html', models.BooleanField(default=False)),
                ('is_system', models.BooleanField(default=False)),
                ('template_type', models.CharField(default='django', max_length=32)),
                ('subject', models.CharField(max_length=200, blank=True)),
                ('description', models.TextField(blank=True)),
            ],
            options={
                'ordering': ('title',),
                'verbose_name': 'Template',
                'verbose_name_plural': 'Template',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Message',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', serialize=False, primary_key=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('subject', models.CharField(max_length=200)),
                ('description', models.TextField(blank=True)),
                ('is_html', models.BooleanField(default=False)),
                ('object_id', models.PositiveIntegerField()),
                ('content_type', models.ForeignKey(to='contenttypes.ContentType')),
                ('template', models.ForeignKey(null=True, blank=True, to='mail.MailTemplate')),
            ],
            options={
                'ordering': ['-created'],
                'verbose_name': 'Mail message',
                'verbose_name_plural': 'Mail messages',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Notify',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', serialize=False, primary_key=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('email', models.EmailField(max_length=75)),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='mail',
            name='message',
            field=models.ForeignKey(to='mail.Message'),
            preserve_default=True,
        ),
    ]
