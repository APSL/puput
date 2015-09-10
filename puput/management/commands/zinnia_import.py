# -*- coding: utf-8 -*-
import os
from django import VERSION as DJANGO_VERSION
from django.contrib.contenttypes.models import ContentType
from django.core.management import BaseCommand
from django.conf import settings
from django.core.files import File
from wagtail.wagtailcore.models import Page, Site
from puput.models import Category as PuputCategory
from puput.models import CategoryEntryPage as PuputCategoryEntryPage
from zinnia.models import Category as ZinniaCategory
from zinnia.models import Entry as ZinniaEntry
from puput.models import EntryPage
from puput.models import TagEntryPage as PuputTagEntryPage
from puput.models import Tag as PuputTag
from wagtail.wagtailimages.models import Image as WagtailImage


class Command(BaseCommand):
    help = "Load Puput data from zinnia blog app"

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

        rootpage.add_child(instance=blogpage)
        revision = rootpage.save_revision()
        revision.publish()

        print("Importing categories...")
        categories = ZinniaCategory.objects.all()
        for category in categories:
            print("\t%s" % category)
            new_category, created  = PuputCategory.objects.update_or_create(
                name=category.title,
                slug=category.slug,
                description=category.description
            )
            new_category.save()

        print("Importing entries...")
        entries = ZinniaEntry.objects.all()
        for entry in entries:

            print entry.title

            # Header images
            if entry.image:
                header_image = WagtailImage(file=entry.image, title=os.path.basename(entry.image.url))
                print('\tImported header image: {}'.format(entry.image))
                header_image.save()
            else:
                header_image = None

            print('\tGenerate and replace content images....')
            import lxml.html as LH
            root = LH.fromstring(entry.content)
            for el in root.iter('img'):
                if  el.attrib['src'].startswith(settings.MEDIA_URL):
                    old_image = el.attrib['src'].replace(settings.MEDIA_URL, '')
                    image_file = open('{}/{}'.format(settings.MEDIA_ROOT, old_image), 'r')
                    new_image = WagtailImage(file=File(file=image_file, name=os.path.basename(old_image)),
                                             title=os.path.basename(old_image))
                    new_image.save()
                    el.attrib['src'] = new_image.file.url
                    print '\t\t{}'.format(new_image.file.url)

            # New content with images replaced
            content = LH.tostring(root, pretty_print=True)

            # Create page
            page = EntryPage(
                title=entry.title,
                body=content,
                slug=entry.slug,
                first_published_at=entry.start_publication,
                expire_at=entry.end_publication,
                latest_revision_created_at=entry.creation_date,
                date=entry.creation_date,
                owner=entry.authors.first(),
                seo_title=entry.title,
                live=entry.is_visible,
                header_image=header_image
            )

            blogpage.add_child(instance=page)
            revision = blogpage.save_revision()
            revision.publish()

            print("\tImporting categories...")
            for category in entry.categories.all():
                print('\t\tAdd category: %s' % category.title)
                pc = PuputCategory.objects.get(name=category.title)
                PuputCategoryEntryPage(category=pc, page=page)


            print("\tImporting tags...")
            for entry_tag in entry.tags_list: # tags de zinnia
                print('\t\t{}'.format(entry_tag))
                tag, created = PuputTag.objects.update_or_create(name=entry_tag)
                page.entry_tags.add(PuputTagEntryPage(tag=tag))
                page.save()
                page.save_revision()