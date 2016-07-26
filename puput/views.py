from django.http import Http404, HttpResponse
from django.views.generic import View
from django.views.decorators.csrf import ensure_csrf_cookie
from django.utils.decorators import method_decorator

from wagtail.wagtailcore import hooks

from .comments import get_num_comments_with_disqus
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

    @method_decorator(ensure_csrf_cookie)
    def get(self, request, *args, **kwargs):
        if not request.site:
            raise Http404
        if request.resolver_match.url_name == 'entry_page_serve_slug':
            # Splitting the request path and obtaining the path_components
            # this way allows you to place the blog at the level you want on
            # your sitemap.
            # Example:
            # splited_path =  ['es', 'blog', '2016', '06', '23', 'blog-entry']
            # slicing this way you obtain:
            # path_components =  ['es', 'blog', 'blog-entry']
            # with the oldest solution you'll get ['es', 'blog-entry']
            # and a 404 will be raised
            splited_path = request.path.strip("/").split("/")
            path_components = splited_path[:-4] + splited_path[-1:]
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
            num_comments = 0
            if blog_page.disqus_api_secret:
                num_comments = get_num_comments_with_disqus(blog_page, entry_page)
            entry_page.num_comments = num_comments
            entry_page.save()
            return HttpResponse()
        except EntryPage.DoesNotExist:
            raise Http404
