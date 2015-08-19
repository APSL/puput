# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('puput', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='blogpage',
            name='disqus_api_secret',
            field=models.TextField(blank=True),
        ),
        migrations.AddField(
            model_name='blogpage',
            name='disqus_shortname',
            field=models.CharField(max_length=128, blank=True),
        ),
    ]
