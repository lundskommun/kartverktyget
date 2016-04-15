# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('survey', '0002_auto_20151027_1729'),
    ]

    operations = [
        migrations.AddField(
            model_name='survey',
            name='questionnaire',
            field=models.CharField(default=b'F', max_length=1, choices=[(b'F', 'Free-text'), (b'S', 'School trips (original crawls)')]),
        ),
    ]
