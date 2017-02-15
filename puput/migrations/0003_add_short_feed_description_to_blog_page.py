from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('puput', '0002_auto_20150919_0925'),
    ]

    operations = [
        migrations.AddField(
            model_name='blogpage',
            name='short_feed_description',
            field=models.BooleanField(default=True, verbose_name='Use short description in feeds'),
        ),
    ]
