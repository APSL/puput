class CommentsProvider:
    def __init__(self, blog_page, entry_page):
        self.blog_page = blog_page
        self.entry_page = entry_page

    @property
    def template(self):
        raise NotImplementedError()

    def get_context(self):
        raise NotImplementedError()

    def get_num_comments(self):
        raise NotImplementedError()


class DisqusCommentsProvider(CommentsProvider):

    @property
    def template(self):
        return 'puput/comments/disqus.html'

    def get_context(self):
        if not self.blog_page.disqus_shortname:
            return {}
        return {
            'disqus_shortname': self.blog_page.disqus_shortname,
            'disqus_identifier': self.entry_page.id
        }

    def get_num_comments(self):
        if not self.blog_page.disqus_api_secret:
            return 0
        try:
            from tapioca.exceptions import ClientError
            from tapioca_disqus import Disqus

            disqus_client = Disqus(api_secret=self.blog_page.disqus_api_secret)
            try:
                params = {'forum': self.blog_page.disqus_shortname, 'thread': 'ident:{}'.format(self.entry_page.id)}
                thread = disqus_client.threads_details().get(params=params)
                return thread.response.posts().data()
            except ClientError:
                return 0
        except ImportError:
            raise Exception('You need to install tapioca-disqus before using Disqus as comment system.')


class DjangoCommentsProvider(CommentsProvider):

    @property
    def template(self):
        return 'puput/comments/django_comments.html'

    def get_context(self):
        return {
            'entry': self.entry_page
        }

    def get_num_comments(self):
        try:
            from django_comments.models import Comment
            from django.contrib.contenttypes.models import ContentType

            entry_page_type = ContentType.objects.get(app_label='puput', model='entrypage')
            return Comment.objects.filter(content_type=entry_page_type, object_pk=self.entry_page.pk).count()
        except ImportError:
            raise Exception('You need to install django-comments before using it as comment system.')
