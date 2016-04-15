# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('survey', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='survey',
            name='description',
            field=models.TextField(blank=True),
        ),
        migrations.AlterField(
            model_name='survey',
            name='map_center',
            field=models.CharField(default=b'55.7053, 13.1865', max_length=32),
        ),
    ]
