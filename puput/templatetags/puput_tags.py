# -*- coding: utf-8 -*-
from django.core.urlresolvers import reverse
from django.template import Library, loader

from endless_pagination.templatetags.endless import show_pages, paginate

from ..models import Category, Tag

register = Library()


@register.inclusion_tag('puput/tags/entries_list.html', takes_context=True)
def recent_entries(context, limit=None):
    blog_page = context['blog_page']
    entries = blog_page.get_entries().order_by('-date')
    if limit:
        entries = entries[:limit]
    return {'blog_page': blog_page, 'request': context['request'], 'entries': entries}


@register.inclusion_tag('puput/tags/entries_list.html', takes_context=True)
def popular_entries(context, limit=None):
    blog_page = context['blog_page']
    entries = blog_page.get_entries().order_by('-num_comments', '-date')
    if limit:
        entries = entries[:limit]
    return {'blog_page': blog_page, 'request': context['request'], 'entries': entries}


@register.inclusion_tag('puput/tags/tags_list.html', takes_context=True)
def tags_list(context, limit=None, tags_qs=None):
    blog_page = context['blog_page']
    if tags_qs:
        tags = tags_qs.all()
    else:
        tags = Tag.objects.with_uses(blog_page)
    if limit:
        tags = tags[:limit]
    return {'blog_page': blog_page, 'request': context['request'], 'tags': tags}


@register.inclusion_tag('puput/tags/categories_list.html', takes_context=True)
def categories_list(context, categories_qs=None):
    blog_page = context['blog_page']
    if categories_qs:
        categories = categories_qs.all()
    else:
        categories = Category.objects.with_uses(blog_page).filter(parent=None)
    return {'blog_page': blog_page, 'request': context['request'], 'categories': categories}


@register.inclusion_tag('puput/tags/archives_list.html', takes_context=True)
def archives_list(context):
    blog_page = context['blog_page']
    archives = blog_page.get_entries().datetimes('date', 'day', order='DESC')
    return {'blog_page': blog_page, 'request': context['request'], 'archives': archives}


@register.simple_tag()
def entry_url(entry, blog_page):
    return reverse('entry_page_serve', kwargs={
        'blog_slug': blog_page.slug,
        'year': entry.date.strftime('%Y'),
        'month': entry.date.strftime('%m'),
        'day': entry.date.strftime('%d'),
        'slug': entry.slug
    })


@register.simple_tag(takes_context=True)
def show_comments(context):
    blog_page = context['blog_page']
    entry = context['self']
    if blog_page.display_comments:
        if blog_page.disqus_shortname:
            template = loader.get_template('puput/comments/disqus.html')
            return template.render({'disqus_shortname': blog_page.disqus_shortname, 'disqus_identifier': entry.id})
    return ""

# Avoid to import endless_pagination in installed_apps and in the templates
register.tag('show_paginator', show_pages)
register.tag('paginate', paginate)
