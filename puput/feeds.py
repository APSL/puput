# -*- coding: utf-8 -*-
from urlparse import urljoin

from django.contrib.syndication.views import Feed

from wagtail.wagtailcore.models import Site

from .models import BlogPage


class BlogPageFeed(Feed):

    def __call__(self, request, *args, **kwargs):
        self.blog_page = BlogPage.objects.get(slug=kwargs['blog_slug'])
        self.request = request
        return super(BlogPageFeed, self).__call__(request, *args, **kwargs)

    def title(self):
        return self.blog_page.title

    def description(self):
        return self.blog_page.description

    def link(self):
        return self.blog_page.slug

    def items(self):
        return self.blog_page.get_entries()[:20]

    def item_title(self, item):
        return item.title

    def item_description(self, item):
        return item.body

    def item_pubdate(self, item):
        return item.date

    def item_enclosure_url(self, item):
        if item.header_image:
            site = Site.find_for_request(self.request)
            return urljoin(site.root_url, item.header_image.file.url)
        return None
