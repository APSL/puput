import operator
from tapioca.exceptions import ClientError
from tapioca_disqus import Disqus

from django.http import Http404, HttpResponse
from django.views.generic import View

from wagtail.wagtailcore import hooks

from .models import EntryPage


class EntryPageServe(View):
    """
    This class is responsible to serve entries with a proper blog url format:
    http://wwww.example.com/2015/10/01/my-first-post

    If you set your blog as Wagtail Root page, the url is like the above example.
    Otherwise if you have a multiple blog instances, you need to pass the slug of the blog
    page instance that you want to use:
    http://wwww.example.com/weblog/2015/10/01/my-first-post
    http://wwww.example.com/videblog/2015/10/01/my-first-video
    """

    def get(self, request, *args, **kwargs):
        if not request.site:
            raise Http404
        if request.resolver_match.url_name == 'entry_page_serve_slug':
            path_components = list(operator.itemgetter(0, -1)(request.path.strip('/').split('/')))
        else:
            path_components = [request.path.strip('/').split('/')[-1]]
        page, args, kwargs = request.site.root_page.specific.route(request, path_components)

        for fn in hooks.get_hooks('before_serve_page'):
            result = fn(page, request, args, kwargs)
            if isinstance(result, HttpResponse):
                return result
        return page.serve(request, *args, **kwargs)


class EntryPageUpdateCommentsView(View):

    def post(self, request, entry_page_id, *args, **kwargs):
        try:
            entry_page = EntryPage.objects.get(pk=entry_page_id)
            blog_page = entry_page.blog_page
            disqus_client = Disqus(api_secret=blog_page.disqus_api_secret)
            try:
                params = {'forum': blog_page.disqus_shortname, 'thread': 'ident:{}'.format(entry_page_id)}
                thread = disqus_client.threads_details().get(params=params)
                entry_page.num_comments = thread.response.posts().data()
                entry_page.save()
                return HttpResponse()
            except ClientError:
                raise Http404
        except EntryPage.DoesNotExist:
            raise Http404
