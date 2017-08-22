# -*- coding: utf-8 -*-
# Generated by Django 1.10.7 on 2017-04-28 15:25
from __future__ import unicode_literals

from django.db import migrations
import django.db.models.manager
import wagtail.contrib.table_block.blocks
import wagtail.wagtailcore.blocks
import wagtail.wagtailcore.fields
import wagtail.wagtailembeds.blocks
import wagtail.wagtailimages.blocks


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
            name='stream_body',
            field=wagtail.wagtailcore.fields.StreamField((('paragraph', wagtail.wagtailcore.blocks.RichTextBlock()), ('heading', wagtail.wagtailcore.blocks.TextBlock()), ('image', wagtail.wagtailcore.blocks.StructBlock((('image', wagtail.wagtailimages.blocks.ImageChooserBlock()), ('caption', wagtail.wagtailcore.blocks.TextBlock(required=False))))), ('table', wagtail.contrib.table_block.blocks.TableBlock(classname='table')), ('embed', wagtail.wagtailembeds.blocks.EmbedBlock()), ('code', wagtail.wagtailcore.blocks.StructBlock((('language', wagtail.wagtailcore.blocks.ChoiceBlock(choices=[('bash', 'Bash/Shell'), ('css', 'CSS'), ('diff', 'diff'), ('http', 'HTML'), ('javascript', 'Javascript'), ('json', 'JSON'), ('python', 'Python'), ('scss', 'SCSS'), ('yaml', 'YAML')])), ('code', wagtail.wagtailcore.blocks.TextBlock())), label='Code Snippet')), ('markdown', wagtail.wagtailcore.blocks.StructBlock((('markdown', wagtail.wagtailcore.blocks.TextBlock()),), label='Markdown'))), blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='entrypage',
            name='body',
            field=wagtail.wagtailcore.fields.RichTextField(blank=True, verbose_name='body'),
        ),
    ]
