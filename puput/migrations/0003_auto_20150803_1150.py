# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('puput', '0002_initial_data'),
    ]

    operations = [
        migrations.AddField(
            model_name='blogpage',
            name='display_archive',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='blogpage',
            name='display_categories',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='blogpage',
            name='display_comments',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='blogpage',
            name='display_last_entries',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='blogpage',
            name='display_popular_entries',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='blogpage',
            name='display_tags',
            field=models.BooleanField(default=True),
        ),
    ]
