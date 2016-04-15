# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('survey', '0004_auto_20151027_1811'),
    ]

    operations = [
        migrations.AlterField(
            model_name='survey',
            name='description',
            field=models.TextField(help_text='This description is show to the contributors.', verbose_name='description', blank=True),
        ),
    ]
