from django.conf import settings

from .utils import import_model


def update_comment_count(sender, **kwargs):
    comment = kwargs['comment']
    entry_page = comment.content_object
    comment_class = import_model(settings.PUPUT_COMMENTS_PROVIDER)(entry_page.blog_page, entry_page)
    num_comments = comment_class.get_num_comments()
    entry_page.num_comments = num_comments
    entry_page.save(update_fields=('num_comments',))


try:
    from django_comments_xtd.signals import confirmation_received

    confirmation_received.connect(update_comment_count, dispatch_uid="puput_comment_posted_id")
except ImportError:
    pass
