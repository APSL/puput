# -*- coding: utf-8 -*-

from django.db import models
from django.db.models import Count


class TagManager(models.Manager):

    def most_common(self, blog_page):
        entries = blog_page.get_entries()
        return self.filter(entrypage__in=entries).annotate(num_times=Count('entrypage')).order_by('-num_times')


class CategoryManager(models.Manager):

    def with_uses(self, blog_page):
        entries = blog_page.get_entries()
        return self.filter(entrypage__in=entries).distinct()
