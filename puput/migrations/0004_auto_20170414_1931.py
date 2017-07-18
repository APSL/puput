# -*- coding: utf-8 -*-
# Generated by Django 1.10.7 on 2017-04-15 00:31
from __future__ import unicode_literals

from django.db import migrations
import django.db.models.manager
import puput.blocks
import puput.puput_markdown.blocks
import wagtail.wagtailcore.blocks
import wagtail.wagtailcore.fields


class Migration(migrations.Migration):

    dependencies = [
        ('puput', '0003_add_short_feed_description_to_blog_page'),
    ]

    operations = [
        migrations.AlterModelManagers(
            name='blogpage',
            managers=[
                ('extra', django.db.models.manager.Manager()),
            ],
        ),
        migrations.AddField(
            model_name='entrypage',
            name='extra_body',
            field=wagtail.wagtailcore.fields.StreamField((('rich_text', wagtail.wagtailcore.blocks.RichTextBlock(icon='doc-full', label='Rich Text')), ('html', wagtail.wagtailcore.blocks.RawHTMLBlock(icon='site', label='Raw HTML')), ('quote', puput.blocks.QuoteBlock(icon='openquote', label='Quote')), ('code', wagtail.wagtailcore.blocks.StructBlock((('language', wagtail.wagtailcore.blocks.ChoiceBlock(choices=[('bash', 'Bash/Shell'), ('c', 'C'), ('cpp', 'C++'), ('csharp', 'C#'), ('css', 'CSS'), ('diff', 'Diff'), ('erlang', 'Erlang'), ('html', 'HTML'), ('java', 'Java'), ('javascript', 'JavaScript'), ('json', 'JSON'), ('perl', 'Perl'), ('php', 'PHP'), ('python', 'Python'), ('ruby', 'Ruby'), ('scala', 'Scala'), ('scss', 'SCSS'), ('sql', 'SQL'), ('vbnet', 'Visual Basic'), ('xml', 'XML'), ('yaml', 'YAML')])), ('code', wagtail.wagtailcore.blocks.TextBlock(rows=3))), icon='code', label='Code Snippet')), ('markdown', puput.puput_markdown.blocks.MarkdownBlock(icon='code', label='Markdown'))), blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='entrypage',
            name='body',
            field=wagtail.wagtailcore.fields.RichTextField(blank=True, verbose_name='body'),
        ),
    ]
