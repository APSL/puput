from mimetypes import guess_type
from urllib.parse import urljoin

from django import http
from django.contrib.syndication.views import Feed
from django.utils.feedgenerator import Rss201rev2Feed
from django.template.defaultfilters import truncatewords_html
from wagtail.core.models import Site

from .models import BlogPage


class BlogPageFeedGenerator(Rss201rev2Feed):
    def add_root_elements(self, handler):
        super(BlogPageFeedGenerator, self).add_root_elements(handler)
        if self.feed['image_link']:
            handler.addQuickElement(
                'image',
                '',
                {
                    'url': self.feed['image_link'],
                    'title': self.feed['title'],
                    'link': self.feed['link'],
                }
            )


class BlogPageFeed(Feed):
    feed_type = BlogPageFeedGenerator

    def __call__(self, request, *args, **kwargs):
        if request.resolver_match.url_name == 'blog_page_feed_slug':
            self.blog_page = BlogPage.extra.get_by_path(kwargs['blog_path'])
            if not self.blog_page:
                raise http.Http404
        else:
            self.blog_page = BlogPage.objects.first()
        self.request = request
        return super(BlogPageFeed, self).__call__(request, *args, **kwargs)

    def title(self):
        return self.blog_page.title

    def description(self):
        return self.blog_page.description

    def link(self):
        return self.blog_page.last_url_part

    def items(self):
        return self.blog_page.get_entries()[:20]

    def item_title(self, item):
        return item.title

    def _item_short_description(self, item):
        if item.excerpt and item.excerpt.strip() != '':
            return item.excerpt
        else:
            return truncatewords_html(item.body, 70)

    def item_description(self, item):
        if self.blog_page.short_feed_description:
            return self._item_short_description(item)
        return item.body

    def item_pubdate(self, item):
        return item.date

    def item_link(self, item):
        from .urls import get_entry_url
        entry_url = get_entry_url(item, self.blog_page.page_ptr, Site.find_for_request(self.request).root_page)
        return self.request.build_absolute_uri(entry_url)

    def item_enclosure_url(self, item):
        if item.header_image:
            site = Site.find_for_request(self.request)
            return urljoin(site.root_url, item.header_image.file.url)
        return None

    def item_enclosure_mime_type(self, item):
        if item.header_image:
            mime, enc = guess_type(self.item_enclosure_url(item))
            return mime
        return None

    def item_enclosure_length(self, item):
        if item.header_image:
            return item.header_image.file.size
        return 0

    def _channel_image_link(self):
        if self.blog_page.header_image:
            site = Site.find_for_request(self.request)
            return urljoin(site.root_url, self.blog_page.header_image.file.url)

    def feed_extra_kwargs(self, obj):
        return {
            'image_link': self._channel_image_link()
        }
