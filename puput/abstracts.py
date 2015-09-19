import datetime

from django.db import models
from django.utils.translation import ugettext_lazy as _

from modelcluster.contrib.taggit import ClusterTaggableManager
from wagtail.wagtailcore.fields import RichTextField


class EntryAbstract(models.Model):
    body = RichTextField(verbose_name=_('body'))
    tags = ClusterTaggableManager(through='puput.TagEntryPage', blank=True)
    date = models.DateTimeField(verbose_name=_("Post date"), default=datetime.datetime.today)
    header_image = models.ForeignKey('wagtailimages.Image', verbose_name=_('Header image'), null=True, blank=True,
                                     on_delete=models.SET_NULL, related_name='+', )
    categories = models.ManyToManyField('puput.Category', through='puput.CategoryEntryPage', blank=True)
    excerpt = RichTextField(verbose_name=_('excerpt'), blank=True,
                            help_text=_("Entry excerpt to be displayed on entries list. "
                                        "If this field is not filled, a truncate version of body text will be used."))
    num_comments = models.IntegerField(default=0, editable=False)

    class Meta:
        abstract = True
