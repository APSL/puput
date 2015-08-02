# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import modelcluster.fields
import datetime
import django.db.models.deletion
import modelcluster.contrib.taggit
import wagtail.wagtailcore.fields
import puput.routes


class Migration(migrations.Migration):

    dependencies = [
        ('wagtailcore', '0001_squashed_0016_change_page_url_path_to_text_field'),
        ('wagtailimages', '0006_add_verbose_names'),
        ('taggit', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='BlogPage',
            fields=[
                ('page_ptr', models.OneToOneField(parent_link=True, auto_created=True, serialize=False, primary_key=True, to='wagtailcore.Page')),
                ('description', models.CharField(help_text='The page description that will appear under the title.', max_length=255, blank=True, verbose_name='Description')),
                ('header_image', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.SET_NULL, to='wagtailimages.Image', null=True, related_name='+', verbose_name='Header image')),
            ],
            options={
                'verbose_name': 'Blog',
            },
            bases=(puput.routes.BlogRoutes, 'wagtailcore.page'),
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, primary_key=True, verbose_name='ID')),
                ('name', models.CharField(max_length=80, unique=True, verbose_name='Category Name')),
                ('slug', models.SlugField(max_length=80, unique=True)),
                ('description', models.CharField(max_length=500, blank=True)),
                ('parent', models.ForeignKey(blank=True, null=True, related_name='children', to='puput.Category')),
            ],
            options={
                'ordering': ['name'],
                'verbose_name_plural': 'Categories',
                'verbose_name': 'Category',
            },
        ),
        migrations.CreateModel(
            name='CategoryEntryPage',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, primary_key=True, verbose_name='ID')),
                ('category', models.ForeignKey(to='puput.Category', related_name='+', verbose_name='Category')),
            ],
        ),
        migrations.CreateModel(
            name='EntryPage',
            fields=[
                ('page_ptr', models.OneToOneField(parent_link=True, auto_created=True, serialize=False, primary_key=True, to='wagtailcore.Page')),
                ('body', wagtail.wagtailcore.fields.RichTextField(verbose_name='body')),
                ('date', models.DateTimeField(default=datetime.datetime.today, verbose_name='Post date')),
                ('excerpt', wagtail.wagtailcore.fields.RichTextField(help_text='Used to display on puput pages list. If this field is not filled, a truncate version of body text will be used.', blank=True, verbose_name='excerpt')),
                ('num_comments', models.IntegerField(default=0, editable=False)),
                ('categories', models.ManyToManyField(blank=True, to='puput.Category', through='puput.CategoryEntryPage')),
                ('header_image', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.SET_NULL, to='wagtailimages.Image', null=True, related_name='+', verbose_name='Header image')),
            ],
            options={
                'verbose_name_plural': 'Entries',
                'verbose_name': 'Entry',
            },
            bases=('wagtailcore.page',),
        ),
        migrations.CreateModel(
            name='EntryPageRelated',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, primary_key=True, verbose_name='ID')),
                ('entrypage_from', modelcluster.fields.ParentalKey(to='puput.EntryPage', related_name='related_entrypage_from', verbose_name='Entry')),
                ('entrypage_to', modelcluster.fields.ParentalKey(to='puput.EntryPage', related_name='related_entrypage_to', verbose_name='Entry')),
            ],
        ),
        migrations.CreateModel(
            name='TagEntryPage',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, primary_key=True, verbose_name='ID')),
                ('content_object', modelcluster.fields.ParentalKey(to='puput.EntryPage', related_name='entry_tags')),
            ],
            options={
                'abstract': False,
            },
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
        migrations.AddField(
            model_name='tagentrypage',
            name='tag',
            field=models.ForeignKey(to='taggit.Tag', related_name='puput_tagentrypage_items'),
        ),
        migrations.AddField(
            model_name='entrypage',
            name='tags',
            field=modelcluster.contrib.taggit.ClusterTaggableManager(help_text='A comma-separated list of tags.', blank=True, through='puput.TagEntryPage', to='taggit.Tag', verbose_name='Tags'),
        ),
        migrations.AddField(
            model_name='categoryentrypage',
            name='page',
            field=modelcluster.fields.ParentalKey(to='puput.EntryPage', related_name='entry_categories'),
        ),
    ]
