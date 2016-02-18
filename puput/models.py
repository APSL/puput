# -*- coding: utf-8 -*-

from django.conf import settings

from django.core.exceptions import ValidationError
from django.db import models
from django.template.defaultfilters import slugify
from django.utils.translation import ugettext_lazy as _
from django.utils.encoding import python_2_unicode_compatible

from wagtail.wagtailcore.models import Page
from wagtail.wagtailadmin.edit_handlers import FieldPanel, MultiFieldPanel
from wagtail.wagtailimages.edit_handlers import ImageChooserPanel
from wagtail.wagtailsnippets.models import register_snippet
from wagtail.wagtailsearch import index
from taggit.models import TaggedItemBase, Tag as TaggitTag
from modelcluster.fields import ParentalKey

from .abstracts import EntryAbstract
from .utils import import_model
from .routes import BlogRoutes
from .managers import TagManager, CategoryManager

Entry = import_model(getattr(settings, 'PUPUT_ENTRY_MODEL', EntryAbstract))


class BlogPage(BlogRoutes, Page):
    description = models.CharField(verbose_name=_('Description'), max_length=255, blank=True,
                                   help_text=_("The blog description that will appear under the title."))
    header_image = models.ForeignKey('wagtailimages.Image', verbose_name=_('Header image'), null=True, blank=True,
                                     on_delete=models.SET_NULL, related_name='+')

    display_comments = models.BooleanField(default=False, verbose_name=_('Display comments'))
    display_categories = models.BooleanField(default=True, verbose_name=_('Display categories'))
    display_tags = models.BooleanField(default=True, verbose_name=_('Display tags'))
    display_popular_entries = models.BooleanField(default=True, verbose_name=_('Display popular entries'))
    display_last_entries = models.BooleanField(default=True, verbose_name=_('Display last entries'))
    display_archive = models.BooleanField(default=True, verbose_name=_('Display archive'))

    disqus_api_secret = models.TextField(blank=True)
    disqus_shortname = models.CharField(max_length=128, blank=True)

    num_entries_page = models.IntegerField(default=5, verbose_name=_('Entries per page'))
    num_last_entries = models.IntegerField(default=3, verbose_name=_('Last entries limit'))
    num_popular_entries = models.IntegerField(default=3, verbose_name=_('Popular entries limit'))
    num_tags_entry_header = models.IntegerField(default=5, verbose_name=_('Tags limit entry header'))

    content_panels = Page.content_panels + [
        FieldPanel('description', classname="full"),
        ImageChooserPanel('header_image'),
    ]
    settings_panels = Page.settings_panels + [
        MultiFieldPanel([
            FieldPanel('display_categories'),
            FieldPanel('display_tags'),
            FieldPanel('display_popular_entries'),
            FieldPanel('display_last_entries'),
            FieldPanel('display_archive'),
        ], heading=_("Widgets")),
        MultiFieldPanel([
            FieldPanel('num_entries_page'),
            FieldPanel('num_last_entries'),
            FieldPanel('num_popular_entries'),
            FieldPanel('num_tags_entry_header'),
        ], heading=_("Parameters")),
        MultiFieldPanel([
            FieldPanel('display_comments'),
            FieldPanel('disqus_api_secret'),
            FieldPanel('disqus_shortname'),
        ], heading=_("Comments")),
    ]
    subpage_types = ['puput.EntryPage']

    def get_entries(self):
        field_name = 'owner__%s' % getattr(settings, 'PUPUT_USERNAME_FIELD', 'username')
        return EntryPage.objects.descendant_of(self).live().order_by('-date').select_related(field_name)

    def get_context(self, request, *args, **kwargs):
        context = super(BlogPage, self).get_context(request, *args, **kwargs)
        context['entries'] = self.entries
        context['blog_page'] = self
        context['search_type'] = getattr(self, 'search_type', "")
        context['search_term'] = getattr(self, 'search_term', "")
        return context

    class Meta:
        verbose_name = _('Blog')


@register_snippet
@python_2_unicode_compatible
class Category(models.Model):
    name = models.CharField(max_length=80, unique=True, verbose_name=_('Category name'))
    slug = models.SlugField(unique=True, max_length=80)
    parent = models.ForeignKey('self', blank=True, null=True, related_name="children",
                               verbose_name=_('Parent category'))
    description = models.CharField(max_length=500, blank=True, verbose_name=_('Description'))

    objects = CategoryManager()

    def __str__(self):
        return self.name

    def clean(self):
        if self.parent:
            parent = self.parent
            if self.parent == self:
                raise ValidationError(_('Parent category cannot be self.'))
            if parent.parent and parent.parent == self:
                raise ValidationError(_('Cannot have circular Parents.'))

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        return super(Category, self).save(*args, **kwargs)

    class Meta:
        ordering = ['name']
        verbose_name = _("Category")
        verbose_name_plural = _("Categories")


class CategoryEntryPage(models.Model):
    category = models.ForeignKey(Category, related_name="+", verbose_name=_('Category'))
    page = ParentalKey('EntryPage', related_name='entry_categories')
    panels = [
        FieldPanel('category')
    ]


class TagEntryPage(TaggedItemBase):
    content_object = ParentalKey('EntryPage', related_name='entry_tags')


@register_snippet
class Tag(TaggitTag):
    objects = TagManager()

    class Meta:
        proxy = True


class EntryPageRelated(models.Model):
    entrypage_from = ParentalKey('EntryPage', verbose_name=_("Entry"), related_name='related_entrypage_from')
    entrypage_to = ParentalKey('EntryPage', verbose_name=_("Entry"), related_name='related_entrypage_to')


class EntryPage(Page, Entry):
    # Search
    search_fields = Page.search_fields + (
        index.SearchField('body'),
        index.SearchField('excerpt'),
        index.FilterField('page_ptr_id')
    )

    # Panels
    content_panels = getattr(Entry, 'content_panels', [])

    promote_panels = Page.promote_panels + getattr(Entry, 'promote_panels', [])

    settings_panels = Page.settings_panels + [
        FieldPanel('date'),
        FieldPanel('owner'),
    ] + getattr(Entry, 'settings_panels', [])

    # Parent and child settings
    parent_page_types = ['puput.BlogPage']
    subpage_types = []

    @property
    def blog_page(self):
        return BlogPage.objects.ancestor_of(self).first()

    @property
    def related(self):
        return [related.entrypage_to for related in self.related_entrypage_from.all()]

    @property
    def has_related(self):
        return self.related_entrypage_from.count() > 0

    def get_context(self, request, *args, **kwargs):
        context = super(EntryPage, self).get_context(request, *args, **kwargs)
        context['blog_page'] = self.blog_page
        return context

    class Meta:
        verbose_name = _('Entry')
        verbose_name_plural = _('Entries')
EntryPage._meta.get_field('owner').editable = True
