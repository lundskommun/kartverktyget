# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('survey', '0003_survey_questionnaire'),
    ]

    operations = [
        migrations.AlterField(
            model_name='survey',
            name='created',
            field=models.DateTimeField(auto_now_add=True, verbose_name='created'),
        ),
        migrations.AlterField(
            model_name='survey',
            name='description',
            field=models.TextField(verbose_name='description', blank=True),
        ),
        migrations.AlterField(
            model_name='survey',
            name='map_center',
            field=models.CharField(default=b'55.7053, 13.1865', help_text='Map center is where to center the map when the user first arrives. Defaults to 55.7053, 13.1865 (central Lund).', max_length=32, verbose_name='map center'),
        ),
        migrations.AlterField(
            model_name='survey',
            name='published',
            field=models.BooleanField(default=False, help_text='Decides if the survey should be available to contributors.', verbose_name='published'),
        ),
        migrations.AlterField(
            model_name='survey',
            name='questionnaire',
            field=models.CharField(default=b'F', help_text=b'Decides which questionnaire to use.', max_length=1, verbose_name='questionnaire', choices=[(b'F', 'Free-text'), (b'S', 'School trips (original crawls)')]),
        ),
        migrations.AlterField(
            model_name='survey',
            name='slug',
            field=models.SlugField(help_text='Slug, or short-name. Used in URLs. Needs to be unique.', unique=True, verbose_name='slug'),
        ),
        migrations.AlterField(
            model_name='survey',
            name='title',
            field=models.CharField(help_text='This title is shown to all users.', max_length=60, verbose_name='title'),
        ),
    ]
