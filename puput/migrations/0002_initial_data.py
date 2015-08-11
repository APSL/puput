# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations
from django import VERSION as DJANGO_VERSION


def load_initial_data(apps, schema_editor):
    from django.apps import apps
    Page = apps.get_model("wagtailcore", "Page")
    ContentType = apps.get_model('contenttypes.ContentType')

    # Get blogpage content type
    blogpage_content_type, created = ContentType.objects.get_or_create(
        model='blogpage',
        app_label='puput',
        defaults={'name': 'page'} if DJANGO_VERSION < (1, 8) else {}
    )

    # Edit home page
    homepage = Page.objects.get(slug='home')
    homepage.title = "Puput blog manager"
    homepage.save()

    # Create example blog page
    blogpage = Page(
        title="Blog",
        content_type=blogpage_content_type,
        slug='blog',
    )

    # Add blog page as a child for homepage
    homepage.add_child(instance=blogpage)
    revision = blogpage.save_revision()
    revision.publish()


class Migration(migrations.Migration):

    dependencies = [
        ('puput', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(load_initial_data),
    ]
