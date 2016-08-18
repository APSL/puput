# -*- coding: utf-8 -*-

from django.db import models
from django.db.models import Count
from wagtail.wagtailcore.models import PageManager


class TagManager(models.Manager):

    def most_common(self, blog_page):
        entries = blog_page.get_entries()
        return self.filter(entrypage__in=entries).annotate(num_times=Count('entrypage')).order_by('-num_times')


class CategoryManager(models.Manager):

    def with_uses(self, blog_page):
        entries = blog_page.get_entries()
        return self.filter(entrypage__in=entries).distinct()


class BlogManager(PageManager):

    def get_by_path(self, blog_path):
        # Look for the blog checkin all the path
        from .models import BlogPage
        blogs = BlogPage.objects.filter(slug=blog_path.split("/")[-1])
        for blog in blogs:
            if blog.specific.last_url_part.strip("/") == blog_path:
                return blog.specific
        return

