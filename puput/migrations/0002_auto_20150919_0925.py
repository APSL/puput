# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import wagtail.wagtailcore.fields


class Migration(migrations.Migration):

    dependencies = [
        ('puput', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='blogpage',
            name='description',
            field=models.CharField(max_length=255, help_text='The blog description that will appear under the title.', verbose_name='Description', blank=True),
        ),
        migrations.AlterField(
            model_name='category',
            name='description',
            field=models.CharField(max_length=500, verbose_name='Description', blank=True),
        ),
        migrations.AlterField(
            model_name='category',
            name='name',
            field=models.CharField(max_length=80, unique=True, verbose_name='Category name'),
        ),
        migrations.AlterField(
            model_name='category',
            name='parent',
            field=models.ForeignKey(to='puput.Category', related_name='children', null=True, verbose_name='Parent category', blank=True),
        ),
        migrations.AlterField(
            model_name='entrypage',
            name='excerpt',
            field=wagtail.wagtailcore.fields.RichTextField(help_text='Entry excerpt to be displayed on entries list. If this field is not filled, a truncate version of body text will be used.', verbose_name='excerpt', blank=True),
        ),
    ]
