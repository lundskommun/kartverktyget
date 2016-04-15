# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import ckeditor.fields


class Migration(migrations.Migration):

    dependencies = [
        ('survey', '0008_survey_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='survey',
            name='description',
            field=ckeditor.fields.RichTextField(help_text='This description is show to the contributors.', verbose_name='description', blank=True),
        ),
    ]
