# -*- coding: utf-8 -*-

from django import VERSION as DJANGO_VERSION
from django.contrib.contenttypes.models import ContentType
from django.core.management import BaseCommand

from wagtail.wagtailcore.models import Page, Site


class Command(BaseCommand):
    help = "Load Puput initial dummy data"

    def handle(self, *args, **options):
        # Get blogpage content type
        blogpage_content_type, created = ContentType.objects.get_or_create(
            model='blogpage',
            app_label='puput',
            defaults={'name': 'page'} if DJANGO_VERSION < (1, 8) else {}
        )

        # Get root page
        rootpage = Page.objects.first()

        # Set site root page as root site page
        site = Site.objects.first()
        site.root_page = rootpage
        site.save()

        # Create example blog page
        blogpage = Page(
            title="Blog",
            content_type=blogpage_content_type,
            slug='blog',
        )

        # Add blog page as a child for homepage
        rootpage.add_child(instance=blogpage)
        revision = blogpage.save_revision()
        revision.publish()
