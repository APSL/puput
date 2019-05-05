from django.conf import settings
from django.urls import reverse, path, include

from .feeds import BlogPageFeed
from .views import EntryPageServe, EntryPageUpdateCommentsView
from .utils import strip_prefix_and_ending_slash


urlpatterns = [
    path(
        route='entry_page/<entry_page_id>/update_comments/',
        view=EntryPageUpdateCommentsView.as_view(),
        name='entry_page_update_comments'
    ),
    path(
        route='<path:blog_path>/<int:year>/<int:month>/<int:day>/<str:slug>/',
        view=EntryPageServe.as_view(),
        name='entry_page_serve_slug'
    ),
    path(
        route='<int:year>/<int:month>/<int:day>/<str:slug>/',
        view=EntryPageServe.as_view(),
        name='entry_page_serve'
    ),
    path(
        route='<path:blog_path>/feed/',
        view=BlogPageFeed(),
        name='blog_page_feed_slug'
    ),
    path(
        route='feed/',
        view=BlogPageFeed(),
        name='blog_page_feed'
    )
]

if not getattr(settings, 'PUPUT_AS_PLUGIN', False):
    from wagtail.core import urls as wagtail_urls
    from wagtail.admin import urls as wagtailadmin_urls
    from wagtail.documents import urls as wagtaildocs_urls
    from wagtail.contrib.sitemaps.views import sitemap

    urlpatterns.extend([
        path(
            route='blog_admin/',
            view=include(wagtailadmin_urls)
        ),
        path(
            route='',
            view=include(wagtail_urls)
        ),
        path(
            route='documents/',
            view=include(wagtaildocs_urls)
        ),
        path(
            route='sitemap.xml',
            view=sitemap
        )
    ])


def get_entry_url(entry, blog_page, root_page):
    """
    Get the entry url given and entry page a blog page instances.
    It will use an url or another depending if blog_page is the root page.
    """
    if root_page == blog_page:
        return reverse('entry_page_serve', kwargs={
            'year': entry.date.strftime('%Y'),
            'month': entry.date.strftime('%m'),
            'day': entry.date.strftime('%d'),
            'slug': entry.slug
        })
    else:
        # The method get_url_parts provides a tuple with a custom URL routing
        # scheme. In the last position it finds the subdomain of the blog, which
        # it is used to construct the entry url.
        # Using the stripped subdomain it allows Puput to generate the urls for
        # every sitemap level
        blog_path = strip_prefix_and_ending_slash(blog_page.specific.last_url_part)
        return reverse('entry_page_serve_slug', kwargs={
            'blog_path': blog_path,
            'year': entry.date.strftime('%Y'),
            'month': entry.date.strftime('%m'),
            'day': entry.date.strftime('%d'),
            'slug': entry.slug
        })


def get_feeds_url(blog_page, root_page):
    """
    Get the feeds urls a blog page instance.
    It will use an url or another depending if blog_page is the root page.
    """
    if root_page == blog_page:
        return reverse('blog_page_feed')
    else:
        blog_path = strip_prefix_and_ending_slash(blog_page.specific.last_url_part)
        return reverse('blog_page_feed_slug', kwargs={'blog_path': blog_path})
