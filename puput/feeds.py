# -*- coding: utf-8 -*-
from six.moves import urllib_parse

from django import http
from django.contrib.syndication.views import Feed
from wagtail.wagtailcore.models import Site
from .models import BlogPage


class BlogPageFeed(Feed):

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

    def item_description(self, item):
        return item.body

    def item_pubdate(self, item):
        return item.date

    def item_link(self, item):
        from .urls import get_entry_url
        entry_url = get_entry_url(item, self.blog_page.page_ptr, self.request.site.root_page)
        return self.request.build_absolute_uri(entry_url)

    def item_enclosure_url(self, item):
        if item.header_image:
            site = Site.find_for_request(self.request)
            return urllib_parse.urljoin(site.root_url, item.header_image.file.url)
        return None
