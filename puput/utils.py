from importlib import import_module
from django.urls import reverse


def import_model(path_or_callable):
    if hasattr(path_or_callable, '__call__'):
        return path_or_callable
    else:
        assert isinstance(path_or_callable, str)
        package, attr = path_or_callable.rsplit('.', 1)
        return getattr(import_module(package), attr)


def get_image_model_path():
    from django.conf import settings
    return getattr(settings, 'WAGTAILIMAGES_IMAGE_MODEL', 'wagtailimages.Image')


def strip_prefix_and_ending_slash(path):
    """
    If puput and wagtail are registered with a prefix, it needs to be removed
    so the 'entry_page_serve_slug' or 'blog_page_feed_slug' resolutions can work.
    Ex, here with a dynamic (i18n_patterns()) + a static prefix :
    urlpatterns += i18n_patterns(
        url(r'^blah/', include('puput.urls')),
        url(r'^blah/', include(wagtail_urls)),
    )
    The prefix is simply the root where Wagtail page are served.
    https://github.com/torchbox/wagtail/blob/stable/1.8.x/wagtail/wagtailcore/urls.py#L36
    """
    return path.replace(reverse('wagtail_serve', args=[""]), '', 1).rstrip("/")
