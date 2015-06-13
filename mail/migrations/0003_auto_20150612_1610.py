# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mail', '0002_auto_20150511_1552'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='mailfield',
            options={'verbose_name_plural': 'Mail fields', 'ordering': ['mail', 'key'], 'verbose_name': 'Mail field'},
        ),
    ]
