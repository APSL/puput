from wagtail.wagtailadmin import blocks


class CodeBlock(blocks.TextBlock):

    class Meta:
        template = 'puput/blocks/code.html'
        icon = 'code'
        label = 'Code'


class QuoteBlock(blocks.TextBlock):

    class Meta:
        template = 'puput/blocks/quote.html'
        icon = 'openquote'
        label = "Quote"
