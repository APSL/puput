from django.conf import settings
from django.utils.safestring import mark_safe

from wagtail.wagtailimages.blocks import ImageChooserBlock
from wagtail.wagtailcore.blocks import (
    StructBlock,
    TextBlock,
    StreamBlock,
    RichTextBlock,
    ChoiceBlock,
)
from wagtail.wagtailembeds.blocks import EmbedBlock
from wagtail.contrib.table_block.blocks import TableBlock

from pygments import highlight
from pygments.formatters import get_formatter_by_name
from pygments.lexers import get_lexer_by_name


class CodeBlock(StructBlock):
    """
    A code highlighting block from Puput using Pygments.
    The setting PUPUT_LANGUAGE_CHOICES can be used in Django's settings to
    override the default list of languages provided here.
    """

    LANGUAGE_CHOICES = getattr(
        settings, 'PUPUT_LANGUAGE_CHOICES', (
            ('bash', 'Bash/Shell'),
            ('c', 'C'),
            ('cpp', 'C++'),
            ('csharp', 'C#'),
            ('css', 'CSS'),
            ('diff', 'Diff'),
            ('erlang', 'Erlang'),
            ('html', 'HTML'),
            ('java', 'Java'),
            ('javascript', 'JavaScript'),
            ('json', 'JSON'),
            ('perl', 'Perl'),
            ('php', 'PHP'),
            ('python', 'Python'),
            ('ruby', 'Ruby'),
            ('scala', 'Scala'),
            ('scss', 'SCSS'),
            ('sql', 'SQL'),
            ('vbnet', 'Visual Basic'),
            ('xml', 'XML'),
            ('yaml', 'YAML'),
        )
    )

    language = ChoiceBlock(choices=LANGUAGE_CHOICES)
    code = TextBlock()

    class Meta:
        icon = 'code'

    def render(self, value, context=None):
        src = value['code'].strip('\n')
        lang = value['language']

        lexer = get_lexer_by_name(lang)
        formatter = get_formatter_by_name(
            'html',
            linenos=None,
            cssclass='codehilite',
            style='default',
            noclasses=False,
        )
        return mark_safe(highlight(src, lexer, formatter))


class CaptionedImageBlock(StructBlock):
    image = ImageChooserBlock()
    caption = TextBlock(required=False)

    class Meta:
        icon = 'fa-image'
        template = 'blocks/captioned_image.html'
        help_text = 'Select an image and add a caption (optional).'
