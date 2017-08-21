from django.utils.html import format_html
from django.conf import settings
from wagtail.wagtailcore import hooks


def editor_css():
    return format_html('<link rel="stylesheet" href="{}puput/css/puput_admin_editor.css">'.format(settings.STATIC_URL))
hooks.register('insert_editor_css', editor_css)


@hooks.register('insert_editor_js')
def editor_js():
    script = '<script src="{0}puput/js/toolbar_temporary_fix.js"></script>'
    return script.format(settings.STATIC_URL)
