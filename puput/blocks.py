from django.utils.translation import ugettext_lazy as _

from wagtail.wagtailimages.blocks import ImageChooserBlock
from wagtail.wagtailcore.blocks import (
    StructBlock,
    TextBlock,
    RichTextBlock
)


class CaptionedImageBlock(StructBlock):
    image = ImageChooserBlock()
    caption = TextBlock(required=False)

    class Meta:
        icon = 'image'
        template = 'puput/blocks/captioned_image.html'
        help_text = _('Select an image and add a caption (optional).')


class QuoteBlock(TextBlock):
    """
    Quote simple block that uses a template
    """
    class Meta:
        template = 'puput/blocks/quote.html'
        icon = 'openquote'


class RichTextStructBlock(StructBlock):
    """
    In order to an issue found in StreamFields with RichTextBlock in which the halloeditor takes all the space
    to write and put the icons in the writing area, we found that a temporary solution can be to wrap the RichText
    block inside a StructBlock while wagtail solves it
    Please take a look at:
    - https://github.com/wagtail/wagtail/issues/3587
    - https://github.com/APSL/puput/pull/83
    """
    rich_text = RichTextBlock()

    class Meta:
        icon = 'doc-full'
