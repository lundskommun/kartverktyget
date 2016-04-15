# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('survey', '0005_auto_20151027_1813'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contribution',
            name='created',
            field=models.DateTimeField(auto_now_add=True, verbose_name='created'),
        ),
        migrations.AlterField(
            model_name='contribution',
            name='geometry_data',
            field=models.TextField(help_text='This is the stored geoemetry from the contribution. Not to be edited.', verbose_name='geometry data'),
        ),
        migrations.AlterField(
            model_name='contribution',
            name='ip_address',
            field=models.GenericIPAddressField(help_text='This is the IP address that the contribution originated from.', verbose_name='IP address'),
        ),
        migrations.AlterField(
            model_name='contribution',
            name='questionnaire_data',
            field=models.TextField(help_text='This is the stored responses from the contribution. Not to be edited.', verbose_name='questionnaire data'),
        ),
        migrations.AlterField(
            model_name='contribution',
            name='survey',
            field=models.ForeignKey(verbose_name='survey', to='survey.Survey'),
        ),
        migrations.AlterField(
            model_name='survey',
            name='owner',
            field=models.ForeignKey(verbose_name='user', to=settings.AUTH_USER_MODEL),
        ),
    ]
