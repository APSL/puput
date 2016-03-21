import datetime

from django.db import models
from django.utils.translation import ugettext_lazy as _
from wagtail.wagtailcore.fields import RichTextField, StreamField
from wagtail.wagtailadmin.edit_handlers import FieldPanel, InlinePanel, MultiFieldPanel, StreamFieldPanel
from wagtail.wagtailcore.blocks import RawHTMLBlock, RichTextBlock
from wagtail.wagtailimages.edit_handlers import ImageChooserPanel
from wagtailmarkdown import MarkdownBlock
from modelcluster.contrib.taggit import ClusterTaggableManager

from .blocks import CodeBlock, QuoteBlock


class EntryAbstract(models.Model):
    body = RichTextField(verbose_name=_('body'))
    extra_body = StreamField([
        ('rich_text', RichTextBlock(icon='doc-full', label='Rich Text')),
        ('code', CodeBlock(icon='code')),
        ('quote', QuoteBlock(icon='openquote')),
        ('html', RawHTMLBlock(icon='site', label='HTML')),
        ('markdown', MarkdownBlock(icon="code"))
    ], null=True, blank=True)
    tags = ClusterTaggableManager(through='puput.TagEntryPage', blank=True)
    date = models.DateTimeField(verbose_name=_("Post date"), default=datetime.datetime.today)
    header_image = models.ForeignKey('wagtailimages.Image', verbose_name=_('Header image'), null=True, blank=True,
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
            InlinePanel('related_entrypage_from', label=_("Related Entries")),
        ], heading=_("Metadata")),
    ]

    class Meta:
        abstract = True
