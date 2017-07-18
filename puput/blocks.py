from django.conf import settings
from django.utils.safestring import mark_safe
from wagtail.wagtailcore.blocks import StructBlock, ChoiceBlock, TextBlock
from pygments import highlight
from pygments.formatters import get_formatter_by_name
from pygments.lexers import get_lexer_by_name

from .defaults import PUPUT_PROGRAMMING_LANGUAGE_CHOICES


class CodeBlock(StructBlock):
    """
    A code highlighting block from Puput using Pygments.
    The setting PUPUT_PROGRAMMING_LANGUAGE_CHOICES can be used in Django's settings to
    override the default list of languages provided here.
    """

    LANGUAGE_CHOICES = getattr(settings, 'PUPUT_PROGRAMMING_LANGUAGE_CHOICES', PUPUT_PROGRAMMING_LANGUAGE_CHOICES)

    language = ChoiceBlock(choices=LANGUAGE_CHOICES)
    code = TextBlock(rows=3)

    class Meta:
        icon = 'code'
        label = 'Code Snippet'

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


class QuoteBlock(TextBlock):
    """
    Quote simple block that uses a template
    """
    class Meta:
        template = 'puput/blocks/quote.html'
        icon = 'openquote'
        label = "Quote"
