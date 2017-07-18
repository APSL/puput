from django import forms

from wagtail.utils.widgets import WidgetWithScript


class MarkdownTextarea(WidgetWithScript, forms.widgets.Textarea):
    """
    Textarea that uses SimpleMDE to display a preview of markdown
    """
    def __init__(self, **kwargs):
        super(MarkdownTextarea, self).__init__(**kwargs)

    def render_js_init(self, id_, name, value):
        return 'simplemdeAttach("{0}");'.format(id_)
