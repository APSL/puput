import datetime

from django.db import models
from django.utils.translation import ugettext_lazy as _

from wagtail.wagtailadmin.edit_handlers import (
    FieldPanel, InlinePanel, MultiFieldPanel, PageChooserPanel, StreamFieldPanel
)
from wagtail.wagtailcore.blocks import RichTextBlock, RawHTMLBlock
from wagtail.wagtailimages.edit_handlers import ImageChooserPanel

from modelcluster.contrib.taggit import ClusterTaggableManager
from wagtail.wagtailcore.fields import RichTextField, StreamField

from .puput_markdown.blocks import MarkdownBlock
from .utils import get_image_model_path
from .blocks import CodeBlock, QuoteBlock


class EntryAbstract(models.Model):
    body = RichTextField(verbose_name=_('body'), blank=True)
    extra_body = StreamField([
        ('rich_text', RichTextBlock(icon='doc-full', label=_('Rich Text'))),
        ('html', RawHTMLBlock(icon='site', label=_('Raw HTML'))),
        ('quote', QuoteBlock(icon='openquote', label=_('Quote'))),
        ('code', CodeBlock(icon='code', label=_('Code Snippet'))),
        ('markdown', MarkdownBlock(icon='code', label=_('Markdown')))
    ], null=True, blank=True)
    tags = ClusterTaggableManager(through='puput.TagEntryPage', blank=True)
    date = models.DateTimeField(verbose_name=_("Post date"), default=datetime.datetime.today)
    header_image = models.ForeignKey(get_image_model_path(), verbose_name=_('Header image'), null=True, blank=True,
                                     on_delete=models.SET_NULL, related_name='+', )
    categories = models.ManyToManyField('puput.Category', through='puput.CategoryEntryPage', blank=True)
    excerpt = RichTextField(verbose_name=_('excerpt'), blank=True,
                            help_text=_("Entry excerpt to be displayed on entries list. "
                                        "If this field is not filled, a truncate version of body text will be used."))
    num_comments = models.IntegerField(default=0, editable=False)

    content_panels = [
        MultiFieldPanel([
            FieldPanel('title', classname="title"),
            ImageChooserPanel('header_image'),
            FieldPanel('body', classname="full"),
            StreamFieldPanel('extra_body'),
            FieldPanel('excerpt', classname="full"),
        ], heading=_("Content"), classname="collapsible"),
        MultiFieldPanel([
            FieldPanel('tags'),
            InlinePanel('entry_categories', label=_("Categories")),
            InlinePanel('related_entrypage_from', label=_("Related Entries"),
                        panels=[PageChooserPanel('entrypage_to')]),
        ], heading=_("Metadata")),
    ]

    class Meta:
        abstract = True
