# Generated by Django 4.0 on 2023-05-22 15:01

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('taggit', '0004_alter_taggeditem_content_type_alter_taggeditem_tag'),
        ('puput', '0007_alter_entrypage_body'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tagentrypage',
            name='tag',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='%(app_label)s_%(class)s_items', to='taggit.tag'),
        ),
    ]
