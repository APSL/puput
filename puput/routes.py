# -*- coding: utf-8 -*-

from datetime import date

from django.utils.dateformat import DateFormat
from django.utils.formats import date_format
from django.utils.translation import ugettext_lazy as _

from wagtail.contrib.wagtailroutablepage.models import RoutablePageMixin, route
from wagtail.wagtailcore.models import Page
from wagtail.wagtailsearch.models import Query


class BlogRoutes(RoutablePageMixin):

    @route(r'^(\d{4})/$')
    @route(r'^(\d{4})/(\d{2})/$')
    @route(r'^(\d{4})/(\d{2})/(\d{2})/$')
    def entries_by_date(self, request, year, month=None, day=None, *args, **kwargs):
        self.entries = self.get_entries().filter(date__year=year)
        self.search_type = _('date')
        self.search_term = year
        if month:
            self.entries = self.entries.filter(date__month=month)
            df = DateFormat(date(int(year), int(month), 1))
            self.search_term = df.format('F Y')
        if day:
            self.entries = self.entries.filter(date__day=day)
            self.search_term = date_format(date(int(year), int(month), int(day)))
        return Page.serve(self, request, *args, **kwargs)

    @route(r'^tag/(?P<tag>[-\w]+)/$')
    def entries_by_tag(self, request, tag, *args, **kwargs):
        self.search_type = _('tag')
        self.search_term = tag
        self.entries = self.get_entries().filter(tags__slug=tag)
        return Page.serve(self, request, *args, **kwargs)

    @route(r'^category/(?P<category>[-\w]+)/$')
    def entries_by_category(self, request, category, *args, **kwargs):
        self.search_type = _('category')
        self.search_term = category
        self.entries = self.get_entries().filter(entry_categories__category__slug=category)
        return Page.serve(self, request, *args, **kwargs)

    @route(r'^author/(?P<author>\w+)/$')
    def entries_by_author(self, request, author, *args, **kwargs):
        self.search_type = _('author')
        self.search_term = author
        self.entries = self.get_entries().filter(owner__username=author)
        return Page.serve(self, request, *args, **kwargs)

    @route(r'^search/$')
    def entries_search(self, request, *args, **kwargs):
        search_query = request.GET.get('q', None)
        self.entries = self.get_entries()
        if search_query:
            self.entries = self.entries.search(search_query)
            self.search_term = search_query
            self.search_type = _('search')
            Query.get(search_query).add_hit()
        return Page.serve(self, request, *args, **kwargs)

    @route(r'^$')
    def entries_list(self, request, *args, **kwargs):
        self.entries = self.get_entries()
        return Page.serve(self, request, *args, **kwargs)
