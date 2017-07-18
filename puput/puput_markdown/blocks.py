from django import forms
from django.utils.functional import cached_property
from wagtail.wagtailcore.blocks import TextBlock

from .widgets import MarkdownTextarea
from .utils import render


class MarkdownBlock(TextBlock):
    def __init__(self, **kwargs):
        if 'classname' in kwargs:
            kwargs['classname'] += ' markdown'
        else:
            kwargs['classname'] = 'markdown'
        super(MarkdownBlock, self).__init__(**kwargs)

    @cached_property
    def field(self):
        field_kwargs = {'widget': MarkdownTextarea()}
        field_kwargs.update(self.field_options)
        return forms.CharField(**field_kwargs)

    def render_basic(self, value, context=None):
        return render(value)

    class Media:
        css = {'all': ('puput/plugins/simplemde/simplemde.min.css', )}
        js = (
            'puput/plugins/simplemde/simplemde.min.js',
            'puput/plugins/simplemde/simplemde.attach.js',
        )
