import bleach
import markdown
from django.utils.safestring import mark_safe


def render(text):
    """
    Render method that uses bleach to sanitize html and python-markdown to render the markdown code to html.
    A few extra extensions were added, these can be found on: https://pythonhosted.org/Markdown/extensions/index.html
    """
    return mark_safe(
        bleach.clean(
            markdown.markdown(
                text,
                extensions=[
                    'markdown.extensions.extra',
                    'markdown.extensions.codehilite',
                    'markdown.extensions.nl2br',
                    'markdown.extensions.sane_lists',
                    'markdown.extensions.toc',
                    'markdown.extensions.wikilinks'
                ],
                extension_configs={
                    'codehilite': [
                        ('guess_lang', False),
                    ]
                },
                output_format='html5'
            ),
            tags=[
                'p', 'div', 'span', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'tt', 'pre', 'em', 'strong', 'ul', 'li',
                'dl', 'dd', 'dt', 'code', 'img', 'a', 'table', 'tr', 'th', 'td', 'tbody', 'caption', 'colgroup',
                'thead', 'tfoot', 'blockquote', 'ol', 'hr', 'br'
            ],
            attributes={
                '*': ['class', 'style', 'id'],
                'a': ['href', 'target', 'rel'],
                'img': ['src', 'alt'],
                'tr': ['rowspan', 'colspan'],
                'td': ['rowspan', 'colspan', 'align']
            },
            styles=[
                'color', 'background-color', 'font-family', 'font-weight', 'font-size', 'width', 'height',
                'text-align', 'border', 'border-top', 'border-bottom', 'border-left', 'border-right', 'padding',
                'padding-top', 'padding-bottom', 'padding-left', 'padding-right', 'margin', 'margin-top',
                'margin-bottom', 'margin-left', 'margin-right'
            ]
        )
    )
