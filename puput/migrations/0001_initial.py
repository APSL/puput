# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import modelcluster.contrib.taggit
import datetime
import wagtail.wagtailcore.fields
import modelcluster.fields
import django.db.models.deletion
import puput.routes


class Migration(migrations.Migration):

    dependencies = [
        ('wagtailcore', '0002_auto_20150730_1219'),
        ('taggit', '0001_initial'),
        ('wagtailimages', '0006_add_verbose_names'),
    ]

    operations = [
        migrations.CreateModel(
            name='BlogPage',
            fields=[
                ('page_ptr', models.OneToOneField(parent_link=True, auto_created=True, to='wagtailcore.Page', serialize=False, primary_key=True)),
                ('description', models.CharField(blank=True, max_length=255, help_text='The page description that will appear under the title.', verbose_name='Description')),
                ('display_comments', models.BooleanField(verbose_name='Display comments', default=False)),
                ('display_categories', models.BooleanField(verbose_name='Display categories', default=True)),
                ('display_tags', models.BooleanField(verbose_name='Display tags', default=True)),
                ('display_popular_entries', models.BooleanField(verbose_name='Display popular entries', default=True)),
                ('display_last_entries', models.BooleanField(verbose_name='Display last entries', default=True)),
                ('display_archive', models.BooleanField(verbose_name='Display archive', default=True)),
                ('header_image', models.ForeignKey(blank=True, verbose_name='Header image', on_delete=django.db.models.deletion.SET_NULL, to='wagtailimages.Image', related_name='+', null=True)),
            ],
            options={
                'verbose_name': 'Blog',
            },
            bases=(puput.routes.BlogRoutes, 'wagtailcore.page'),
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', serialize=False, primary_key=True)),
                ('name', models.CharField(unique=True, max_length=80, verbose_name='Category Name')),
                ('slug', models.SlugField(unique=True, max_length=80)),
                ('description', models.CharField(blank=True, max_length=500)),
                ('parent', models.ForeignKey(blank=True, to='puput.Category', related_name='children', null=True)),
            ],
            options={
                'ordering': ['name'],
                'verbose_name_plural': 'Categories',
                'verbose_name': 'Category',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='CategoryEntryPage',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', serialize=False, primary_key=True)),
                ('category', models.ForeignKey(verbose_name='Category', to='puput.Category', related_name='+')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='EntryPage',
            fields=[
                ('page_ptr', models.OneToOneField(parent_link=True, auto_created=True, to='wagtailcore.Page', serialize=False, primary_key=True)),
                ('body', wagtail.wagtailcore.fields.RichTextField(verbose_name='body')),
                ('date', models.DateTimeField(verbose_name='Post date', default=datetime.datetime.today)),
                ('excerpt', wagtail.wagtailcore.fields.RichTextField(blank=True, verbose_name='excerpt', help_text='Used to display on puput pages list. If this field is not filled, a truncate version of body text will be used.')),
                ('num_comments', models.IntegerField(default=0, editable=False)),
                ('categories', models.ManyToManyField(to='puput.Category', blank=True, through='puput.CategoryEntryPage')),
                ('header_image', models.ForeignKey(blank=True, verbose_name='Header image', on_delete=django.db.models.deletion.SET_NULL, to='wagtailimages.Image', related_name='+', null=True)),
            ],
            options={
                'verbose_name': 'Entry',
                'verbose_name_plural': 'Entries',
            },
            bases=('wagtailcore.page',),
        ),
        migrations.CreateModel(
            name='EntryPageRelated',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', serialize=False, primary_key=True)),
                ('entrypage_from', modelcluster.fields.ParentalKey(verbose_name='Entry', to='puput.EntryPage', related_name='related_entrypage_from')),
                ('entrypage_to', modelcluster.fields.ParentalKey(verbose_name='Entry', to='puput.EntryPage', related_name='related_entrypage_to')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='TagEntryPage',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', serialize=False, primary_key=True)),
                ('content_object', modelcluster.fields.ParentalKey(related_name='entry_tags', to='puput.EntryPage')),
                ('tag', models.ForeignKey(related_name='puput_tagentrypage_items', to='taggit.Tag')),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='entrypage',
            name='tags',
            field=modelcluster.contrib.taggit.ClusterTaggableManager(blank=True, verbose_name='Tags', help_text='A comma-separated list of tags.', to='taggit.Tag', through='puput.TagEntryPage'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='categoryentrypage',
            name='page',
            field=modelcluster.fields.ParentalKey(related_name='entry_categories', to='puput.EntryPage'),
            preserve_default=True,
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
            ],
            options={
                'proxy': True,
            },
            bases=('taggit.tag',),
        ),
    ]
