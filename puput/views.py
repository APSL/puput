from django.conf import settings
from django.http import Http404, HttpResponse
from django.views.generic import View
from django.views.decorators.csrf import ensure_csrf_cookie
from django.utils.decorators import method_decorator

from wagtail.core import hooks
from wagtail.core.models import Site

from .models import EntryPage
from .utils import strip_prefix_and_ending_slash, import_model


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
        site = Site.find_for_request(request)
        if not site:
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
            splited_path = strip_prefix_and_ending_slash(request.path).split("/")
            path_components = splited_path[:-4] + splited_path[-1:]
        else:
            path_components = [strip_prefix_and_ending_slash(request.path).split('/')[-1]]
        page, args, kwargs = site.root_page.specific.route(request, path_components)

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
            comment_class = import_model(settings.PUPUT_COMMENTS_PROVIDER)(blog_page, entry_page)
            num_comments = comment_class.get_num_comments()
            entry_page.num_comments = num_comments
            entry_page.save(update_fields=('num_comments',))
            return HttpResponse()
        except EntryPage.DoesNotExist:
            raise Http404
