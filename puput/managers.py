# -*- coding: utf-8 -*-

from django.db import models


class TagManager(models.Manager):

    def with_uses(self, blog_page):
        return self.filter(entrypage__in=blog_page.get_entries()).distinct()


class CategoryManager(models.Manager):

    def with_uses(self, blog_page):
        return self.filter(entrypage__in=blog_page.get_entries()).distinct()
