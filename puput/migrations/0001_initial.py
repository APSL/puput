# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import wagtail.wagtailcore.fields
import modelcluster.fields
import puput.routes
import datetime
import django.db.models.deletion
import modelcluster.contrib.taggit


class Migration(migrations.Migration):

    dependencies = [
        ('wagtailcore', '0001_squashed_0016_change_page_url_path_to_text_field'),
        ('wagtailimages', '0006_add_verbose_names'),
    ]

    operations = [
        migrations.CreateModel(
            name='BlogPage',
            fields=[
                ('page_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='wagtailcore.Page')),
                ('description', models.CharField(help_text='The page description that will appear under the title.', max_length=255, verbose_name='Description', blank=True)),
                ('display_comments', models.BooleanField(default=False, verbose_name='Display comments')),
                ('display_categories', models.BooleanField(default=True, verbose_name='Display categories')),
                ('display_tags', models.BooleanField(default=True, verbose_name='Display tags')),
                ('display_popular_entries', models.BooleanField(default=True, verbose_name='Display popular entries')),
                ('display_last_entries', models.BooleanField(default=True, verbose_name='Display last entries')),
                ('display_archive', models.BooleanField(default=True, verbose_name='Display archive')),
                ('disqus_api_secret', models.TextField(blank=True)),
                ('disqus_shortname', models.CharField(max_length=128, blank=True)),
                ('num_entries_page', models.IntegerField(default=5, verbose_name='Entries per page')),
                ('num_last_entries', models.IntegerField(default=3, verbose_name='Last entries limit')),
                ('num_popular_entries', models.IntegerField(default=3, verbose_name='Popular entries limit')),
                ('num_tags_entry_header', models.IntegerField(default=5, verbose_name='Tags limit entry header')),
                ('header_image', models.ForeignKey(related_name='+', on_delete=django.db.models.deletion.SET_NULL, verbose_name='Header image', blank=True, to='wagtailimages.Image', null=True)),
            ],
            options={
                'verbose_name': 'Blog',
            },
            bases=(puput.routes.BlogRoutes, 'wagtailcore.page'),
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(unique=True, max_length=80, verbose_name='Category Name')),
                ('slug', models.SlugField(unique=True, max_length=80)),
                ('description', models.CharField(max_length=500, blank=True)),
                ('parent', models.ForeignKey(related_name='children', blank=True, to='puput.Category', null=True)),
            ],
            options={
                'ordering': ['name'],
                'verbose_name': 'Category',
                'verbose_name_plural': 'Categories',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='CategoryEntryPage',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('category', models.ForeignKey(related_name='+', verbose_name='Category', to='puput.Category')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='EntryPage',
            fields=[
                ('page_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='wagtailcore.Page')),
                ('body', wagtail.wagtailcore.fields.RichTextField(verbose_name='body')),
                ('date', models.DateTimeField(default=datetime.datetime.today, verbose_name='Post date')),
                ('excerpt', wagtail.wagtailcore.fields.RichTextField(help_text='Used to display on puput pages list. If this field is not filled, a truncate version of body text will be used.', verbose_name='excerpt', blank=True)),
                ('num_comments', models.IntegerField(default=0, editable=False)),
                ('categories', models.ManyToManyField(to='puput.Category', through='puput.CategoryEntryPage', blank=True)),
                ('header_image', models.ForeignKey(related_name='+', on_delete=django.db.models.deletion.SET_NULL, verbose_name='Header image', blank=True, to='wagtailimages.Image', null=True)),
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
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('entrypage_from', modelcluster.fields.ParentalKey(related_name='related_entrypage_from', verbose_name='Entry', to='puput.EntryPage')),
                ('entrypage_to', modelcluster.fields.ParentalKey(related_name='related_entrypage_to', verbose_name='Entry', to='puput.EntryPage')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='TagEntryPage',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
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
            field=modelcluster.contrib.taggit.ClusterTaggableManager(to='taggit.Tag', through='puput.TagEntryPage', blank=True, help_text='A comma-separated list of tags.', verbose_name='Tags'),
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
