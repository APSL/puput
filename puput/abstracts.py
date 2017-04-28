import datetime

from django.db import models
from django.utils.translation import ugettext_lazy as _

from wagtail.wagtailadmin.edit_handlers import (
    FieldPanel,
    InlinePanel,
    MultiFieldPanel,
    PageChooserPanel,
    StreamFieldPanel
)
from wagtail.wagtailimages.edit_handlers import ImageChooserPanel
from wagtail.wagtailcore.fields import RichTextField, StreamField
from wagtail.wagtailcore.blocks import (
    TextBlock,
    RichTextBlock,
)
from wagtail.wagtailembeds.blocks import EmbedBlock
from wagtail.contrib.table_block.blocks import TableBlock

from modelcluster.contrib.taggit import ClusterTaggableManager
from wagtailcodeblock.blocks import CodeBlock
from wagtailmarkdownblock.blocks import MarkdownBlock

from .blocks import CaptionedImageBlock
from .settings import get_use_body, get_use_stream_body
from .utils import get_image_model_path


class EntryAbstract(models.Model):
    body = RichTextField(verbose_name=_('body'), blank=True)
    stream_body = StreamField([
        ('paragraph', RichTextBlock()),
        ('heading', TextBlock()),
        ('image', CaptionedImageBlock()),
        ('table', TableBlock(classname='table')),
        ('embed', EmbedBlock()),
        ('code', CodeBlock(label='Code')),
        ('markdown', MarkdownBlock(label='Markdown')),
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

    main_panels = [
        FieldPanel('title', classname="title"),
        ImageChooserPanel('header_image'),
    ]

    if get_use_body():
        main_panels += [
            FieldPanel('body', classname="full"),
        ]
    if get_use_stream_body():
        main_panels += [
            StreamFieldPanel('stream_body'),
        ]

    main_panels += [
        FieldPanel('excerpt', classname="full"),
    ]

    content_panels = [
        MultiFieldPanel(
            main_panels,
            heading=_("Content")
        ),
        MultiFieldPanel([
            FieldPanel('tags'),
            InlinePanel('entry_categories', label=_("Categories")),
            InlinePanel('related_entrypage_from', label=_("Related Entries"),
                        panels=[PageChooserPanel('entrypage_to')]),
        ], heading=_("Metadata")),
    ]

    class Meta:
        abstract = True
