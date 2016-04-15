# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('survey', '0006_auto_20151102_1533'),
    ]

    operations = [
        migrations.AlterField(
            model_name='survey',
            name='owner',
            field=models.ForeignKey(verbose_name='user', to=settings.AUTH_USER_MODEL, help_text='This is the user currently owning this survey. If you change this to someone else, and you are not a super-user, then you will not be able to see the survey any longer.'),
        ),
    ]
