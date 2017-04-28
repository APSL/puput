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
        help_text = 'Select an image and add a caption (optional).'
