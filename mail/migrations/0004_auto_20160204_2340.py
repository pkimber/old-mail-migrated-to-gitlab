# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mail', '0003_auto_20150612_1610'),
    ]

    operations = [
        migrations.AlterField(
            model_name='mail',
            name='email',
            field=models.EmailField(max_length=254),
        ),
    ]
