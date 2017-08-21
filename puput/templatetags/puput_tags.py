# -*- coding: utf-8 -*-
from django.template import Library
from django.core.urlresolvers import resolve
from django.template.loader import render_to_string

from el_pagination.templatetags.el_pagination_tags import show_pages, paginate

from ..urls import get_entry_url, get_feeds_url
from ..models import Category, Tag

register = Library()


@register.inclusion_tag('puput/tags/entries_list.html', takes_context=True)
def recent_entries(context, limit=None):
    blog_page = context['blog_page']
    entries = blog_page.get_entries().order_by('-date')
    if limit:
        entries = entries[:limit]
    context['entries'] = entries
    return context


@register.inclusion_tag('puput/tags/entries_list.html', takes_context=True)
def popular_entries(context, limit=None):
    blog_page = context['blog_page']
    entries = blog_page.get_entries().order_by('-num_comments', '-date')
    if limit:
        entries = entries[:limit]
    context['entries'] = entries
    return context


@register.inclusion_tag('puput/tags/tags_list.html', takes_context=True)
def tags_list(context, limit=None, tags_qs=None):
    blog_page = context['blog_page']
    if tags_qs:
        tags = tags_qs.all()
    else:
        tags = Tag.objects.most_common(blog_page)
    if limit:
        tags = tags[:limit]
    context['tags'] = tags
    return context


@register.inclusion_tag('puput/tags/categories_list.html', takes_context=True)
def categories_list(context, categories_qs=None):
    blog_page = context['blog_page']
    if categories_qs:
        categories = categories_qs.all()
    else:
        categories = Category.objects.with_uses(blog_page).filter(parent=None)
    context['categories'] = categories
    return context


@register.inclusion_tag('puput/tags/archives_list.html', takes_context=True)
def archives_list(context):
    blog_page = context['blog_page']
    context['archives'] = blog_page.get_entries().datetimes('date', 'day', order='DESC')
    return context


@register.simple_tag(takes_context=True)
def entry_url(context, entry, blog_page):
    return get_entry_url(entry, blog_page.page_ptr, context['request'].site.root_page)


@register.simple_tag(takes_context=True)
def canonical_url(context, entry=None):
    if entry and resolve(context.request.path_info).url_name == 'wagtail_serve':
        return context.request.build_absolute_uri(entry_url(context, entry, entry.blog_page))
    return context.request.build_absolute_uri()


@register.simple_tag(takes_context=True)
def image_url(context, url):
    return context.request.build_absolute_uri(url)


@register.simple_tag(takes_context=True)
def feeds_url(context, blog_page):
    return get_feeds_url(blog_page.page_ptr, context['request'].site.root_page)


@register.simple_tag(takes_context=True)
def show_comments(context):
    blog_page = context['blog_page']
    entry = context['self']
    if blog_page.display_comments and blog_page.disqus_shortname:
        ctx = {
            'disqus_shortname': blog_page.disqus_shortname,
            'disqus_identifier': entry.id
        }
        return render_to_string('puput/comments/disqus.html', context=ctx)
    return ""

# Avoid to import endless_pagination in installed_apps and in the templates
register.tag('show_paginator', show_pages)
register.tag('paginate', paginate)
