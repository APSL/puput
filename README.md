# Puput

Puput is a powerful and simple Django app to manage a blog system. It uses the awesome Wagtail CMS as content management system.

Puput is the catalan name for [Hoopoe](https://en.wikipedia.org/wiki/Hoopoe) which is indeed a beautiful bird.

![Imgur](http://i.imgur.com/ndZLeWb.png?1)

### Features
* Based on Wagtail CMS and Django
* Fully customizable templates
* Inspired on Wordpress and Zinnia
* SEO friendly urls
* Support for Disqus comments
* Archives, tags & categories results pages
* Search form
* Last & popular entries
* RSS feeds
* Blog post related entries

### Setup

1. Add to `INSTALLED_APPS`. This will include Wagtail apps and other dependencies.
    ```
    from puput import PUPUT_APPS
    
    INSTALLED_APPS +=  PUPUT_APPS
    ```
2. Add extra Wagtail required middlewares
    ```
    MIDDLEWARE_CLASSES = (
        ...
        'wagtail.wagtailcore.middleware.SiteMiddleware',
        'wagtail.wagtailredirects.middleware.RedirectMiddleware',
    )
    ```
3. Add Puput urls at the __bottom__ of the urlpatterns. This also will include Wagtail urls.
    ```
        urlpatterns = [
            ...
            url(r'', include('puput.urls')),
        ]
    ```
4. Run `python manage.py migrate`
5. Open your broswer at http://127.0.0.1:8000/blog/ to view your blog home page. 

### Manage your content

Puput uses the default Wagtail CMS admin page in order to manage the content of the blog. It provides a powerful, clean and modern interface to manage your content. Just open your browser at http://127.0.0.1:8000/blog_admin/pages/2/ where you can edit the blog options or add new entries.

This is how adding entry page looks:

![Imgur](http://i.imgur.com/NntrN3i.png?1)

Please visit [Wagtail: an Editor’s guide](http://docs.wagtail.io/en/v1.0/editor_manual/index.html) for the details of how to use Wagtail editor's dashboard.

### Comments

Puput uses django-disqus by default in order to display a comment box in every blog entry. Simply add `DISQUS_API_KEY` and `DISQUS_WEBSITE_SHORTNAME` to `settings.py`. See [django-disqus official documentation](http://django-disqus.readthedocs.org/en/latest/installation.html#configuring-your-django-installation) for more info.

### TODO

* Tests
* More documentation
* Remove django-endless-pagination package which is no longer mantained