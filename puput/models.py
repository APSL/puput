from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models
from django.template.defaultfilters import slugify
from django.utils.translation import gettext_lazy as _

from wagtail.core.models import Page
from wagtail.admin.edit_handlers import FieldPanel
from wagtail.snippets.models import register_snippet
from wagtail.search import index
from taggit.models import TaggedItemBase, Tag as TaggitTag
from modelcluster.fields import ParentalKey

from .abstracts import EntryAbstract, BlogAbstract
from .utils import import_model
from .routes import BlogRoutes
from .managers import TagManager, CategoryManager, BlogManager

Entry = import_model(getattr(settings, 'PUPUT_ENTRY_MODEL', EntryAbstract))
Blog = import_model(getattr(settings, 'PUPUT_BLOG_MODEL', BlogAbstract))


class BlogPage(BlogRoutes, Page, Blog):
    extra = BlogManager()

    content_panels = Page.content_panels + getattr(Blog, 'content_panels', [])
    settings_panels = Page.settings_panels + getattr(Blog, 'settings_panels', [])

    subpage_types = ['puput.EntryPage']

    def get_entries(self):
        return EntryPage.objects.descendant_of(self).live().order_by('-date').select_related('owner')

    def get_context(self, request, *args, **kwargs):
        context = super(BlogPage, self).get_context(request, *args, **kwargs)
        context['entries'] = self.entries
        context['blog_page'] = self
        context['search_type'] = getattr(self, 'search_type', "")
        context['search_term'] = getattr(self, 'search_term', "")
        return context

    @property
    def last_url_part(self):
        """
        Get the BlogPage url without the domain
        """
        return self.get_url_parts()[-1]

    class Meta:
        verbose_name = _('Blog')


@register_snippet
class Category(models.Model):
    name = models.CharField(max_length=80, unique=True, verbose_name=_('Category name'))
    slug = models.SlugField(unique=True, max_length=80)
    parent = models.ForeignKey(
        'self',
        blank=True,
        null=True,
        related_name="children",
        verbose_name=_('Parent category'),
        on_delete=models.SET_NULL
    )
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
    category = models.ForeignKey(Category, related_name="+", verbose_name=_('Category'), on_delete=models.CASCADE)
    page = ParentalKey('EntryPage', related_name='entry_categories')
    panels = [
        FieldPanel('category')
    ]

    def __str__(self):
        return str(self.category)


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

    def __str__(self):
        return str(self.entrypage_to)


class EntryPage(Entry, Page):
    # Search
    search_fields = Page.search_fields + [
        index.SearchField('body'),
        index.SearchField('excerpt'),
        index.FilterField('page_ptr_id')
    ]

    # Panels
    content_panels = getattr(Entry, 'content_panels', [])

    promote_panels = Page.promote_panels + getattr(Entry, 'promote_panels', [])

    settings_panels = Page.settings_panels + [
        FieldPanel('date'), FieldPanel('owner'),
    ] + getattr(Entry, 'settings_panels', [])

    # Parent and child settings
    parent_page_types = ['puput.BlogPage']
    subpage_types = []

    def get_sitemap_urls(self, request=None):
        from .urls import get_entry_url
        root_url = self.get_url_parts()[1]
        entry_url = get_entry_url(self, self.blog_page.page_ptr, root_url)
        return [
            {
                'location': root_url + entry_url,
                # fall back on latest_revision_created_at if last_published_at is null
                # (for backwards compatibility from before last_published_at was added)
                'lastmod': (self.last_published_at or self.latest_revision_created_at),
            }
        ]

    @property
    def blog_page(self):
        return self.get_parent().specific

    @property
    def related(self):
        return [related.entrypage_to for related in self.related_entrypage_from.all()]

    @property
    def has_related(self):
        return self.related_entrypage_from.count() > 0

    def get_absolute_url(self):
        return self.full_url

    def get_context(self, request, *args, **kwargs):
        context = super(EntryPage, self).get_context(request, *args, **kwargs)
        context['blog_page'] = self.blog_page
        return context

    class Meta:
        verbose_name = _('Entry')
        verbose_name_plural = _('Entries')
