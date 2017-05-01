from django.utils.translation import ugettext_lazy as _

from wagtail.wagtailimages.blocks import ImageChooserBlock
from wagtail.wagtailcore.blocks import (
    StructBlock,
    TextBlock,
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
