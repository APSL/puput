from django.conf import settings
from django.conf.urls import url, include

from .feeds import BlogPageFeed
from .views import EntryPageServe, EntryPageUpdateCommentsView


urlpatterns = [
    url(
        regex=r'^entry_page/(?P<entry_page_id>\d+)/update_comments/$',
        view=EntryPageUpdateCommentsView.as_view(),
        name='entry_page_update_comments'
    ),
    url(
        regex=r'^(?P<blog_slug>[-\w]+)/(?P<year>\d{4})/(?P<month>\d{2})/(?P<day>\d{2})/(?P<slug>[-\w]+)/$',
        view=EntryPageServe.as_view(),
        name='entry_page_serve'
    ),
    url(
        regex=r'^(?P<blog_slug>[-\w]+)/feed/$',
        view=BlogPageFeed(),
        name='blog_page_feed'
    )
]

if not getattr(settings, 'PUPUT_AS_PLUGIN', False):
    from wagtail.wagtailcore import urls as wagtail_urls
    from wagtail.wagtailadmin import urls as wagtailadmin_urls
    from wagtail.wagtaildocs import urls as wagtaildocs_urls
    from wagtail.wagtailsearch import urls as wagtailsearch_urls
    from wagtail.contrib.wagtailsitemaps.views import sitemap

    urlpatterns.extend([
        url(
            regex=r'^blog_admin/',
            view=include(wagtailadmin_urls)
        ),
        url(
            regex=r'',
            view=include(wagtail_urls)
        ),
        url(
            regex=r'^search/',
            view=include(wagtailsearch_urls)
        ),
        url(
            regex=r'^documents/',
            view=include(wagtaildocs_urls)
        ),
        url(
            regex='^sitemap\.xml$',
            view=sitemap
        )
    ])
