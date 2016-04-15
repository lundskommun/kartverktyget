# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('survey', '0007_auto_20151102_1535'),
    ]

    operations = [
        migrations.AddField(
            model_name='survey',
            name='image',
            field=models.ImageField(help_text='Image to be shown in conjunction with your survey.', upload_to=b'', verbose_name='image', blank=True),
        ),
    ]
