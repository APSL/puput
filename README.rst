.. image:: https://readthedocs.org/projects/puput/badge/?version=latest
    :target: https://readthedocs.org/projects/puput/?badge=latest
    :alt: Documentation Status

Puput
=====

Puput is a powerful and simple Django app to manage a blog. It uses the awesome `Wagtail CMS <https://github.com/torchbox/wagtail>`_ as content management system.

Puput is the catalan name for `Hoopoe <https://en.wikipedia.org/wiki/Hoopoe>`_ which is indeed a beautiful bird.

.. image:: http://i.imgur.com/3ByGQb6.png

Features
~~~~~~~~

* Built with Wagtail CMS and Django
* Inspired in Wordpress and Zinnia
* Simple & responsive HTML template by default
* SEO friendly urls
* Support for Disqus comments
* Entries by author, tags, categories, archives and search term
* Last & popular entries
* Configurable sidebar widgets
* RSS feeds
* Related entries
* Extensible entry model

.. image:: http://i.imgur.com/ndZLeWb.png

Setup
~~~~~

If you have a running Django project and you want to add blog site to your project,
please follow **Standalone blog app** steps. Otherwise follow the **Wagtail blog app** steps if you are currently using Wagtail on your project.


Standalone blog app
-------------------
1. Install Puput and its dependencies :code:`pip install puput`

2. Add :code:`PUPUT_APPS` to your :code:`INSTALLED_APPS` in :code:`settings.py` file.

.. code-block:: python

    from puput import PUPUT_APPS

    INSTALLED_APPS += PUPUT_APPS

This includes Puput, `Wagtail apps <http://docs.wagtail.io/en/v1.0/advanced_topics/settings.html#wagtail-apps>`_ and `Third party apps <http://docs.wagtail.io/en/v1.0/advanced_topics/settings.html#third-party-apps>`_.
If you have on of these apps previously defined in your :code:`INSTALLED_APPS` please include manually this apps in order to avoid apps collisions:

.. code-block:: python

    INSTALLED_APPS = (
        ...
        'wagtail.wagtailcore',
        'wagtail.wagtailadmin',
        'wagtail.wagtaildocs',
        'wagtail.wagtailsnippets',
        'wagtail.wagtailusers',
        'wagtail.wagtailimages',
        'wagtail.wagtailembeds',
        'wagtail.wagtailsearch',
        'wagtail.wagtailsites',
        'wagtail.wagtailredirects',
        'wagtail.wagtailforms',
        'wagtail.contrib.wagtailsitemaps',
        'wagtail.contrib.wagtailroutablepage',
        'compressor',
        'taggit',
        'modelcluster',
        'puput',
    )


3. Add Wagtail required middleware classes in :code:`settings.py` file

.. code-block:: python

    MIDDLEWARE_CLASSES = (
        ...
        'wagtail.wagtailcore.middleware.SiteMiddleware',
        'wagtail.wagtailredirects.middleware.RedirectMiddleware',
    )

4. Add :code:`request` context processor to :code:`TEMPLATE_CONTEXT_PROCESSORS` structure in :code:`settings.py` file

.. code-block:: python

    TEMPLATE_CONTEXT_PROCESSORS = (
        ...
        'django.core.context_processors.request',
    )

5. Set :code:`WAGTAIL_SITE_NAME` variable in :code:`settings.py` file with your site name:

.. code-block:: python

    WAGTAIL_SITE_NAME = 'Puput blog'

6. Set :code:`MEDIA_ROOT` and :code:`MEDIA_URL` variable in :code:`settings.py` as described in the `Wagtail Docs <http://docs.wagtail.io/en/v1.1/advanced_topics/settings.html#ready-to-use-example-configuration-files>`_:

.. code-block:: python

    MEDIA_ROOT = os.path.join(PROJECT_ROOT, 'media')
    MEDIA_URL = '/media/'


7. Place Puput urls at the **bottom** of the urlpatterns. It also includes Wagtail urls:

.. code-block:: python

    urlpatterns = [
        ...
        url(r'', include('puput.urls')),
    ]

8. To make your Django project serve your media files (ex: uploaded contents) during development, don't forget to add this to your urlpatterns:

.. code-block:: python


    from django.conf import settings

    if settings.DEBUG:
        import os
        from django.conf.urls import patterns
        from django.conf.urls.static import static
        from django.views.generic.base import RedirectView
        from django.contrib.staticfiles.urls import staticfiles_urlpatterns

        urlpatterns += staticfiles_urlpatterns() # tell gunicorn where static files are in dev mode
        urlpatterns += static(settings.MEDIA_URL + 'images/', document_root=os.path.join(settings.MEDIA_ROOT, 'images'))
        urlpatterns += patterns('',
            (r'^favicon\.ico$', RedirectView.as_view(url=settings.STATIC_URL + 'myapp/images/favicon.ico'))
        )


9. Run :code:`python manage.py migrate` and :code:`python manage.py puput_initial_data` to load initial data to start a blog site.
10. Open your broswer at http://127.0.0.1:8000/blog/ to view your blog home page. Go to http://127.0.0.1:8000/blog_admin/ to view the admin site and edit your content.


Wagtail blog app
----------------
1. Install Puput and its dependencies :code:`pip install puput`
2. Add :code:`puput`, :code:`wagtail.contrib.wagtailsitemaps` and :code:`wagtail.contrib.wagtailroutablepage` to your :code:`INSTALLED_APPS` in :code:`settings.py` file.
3. If you have previously defined Wagtail urls in :code:`urls.py` set :code:`PUPUT_AS_PLUGIN = True` in the :code:`settings.py`. This will avoid to include Wagtail urls again when you include necessary Puput urls.
4. Include Puput urls in :code:`urls.py` **before** Wagtail urls.

.. code-block:: python

    urlpatterns = [
        ...
        url(r'', include('puput.urls')),
        url(r'', include(wagtail_urls)),
    ]

5. Run :code:`python manage.py migrate`

Documentation
~~~~~~~~~~~~~
Visit `Puput documentation <http://puput.readthedocs.org>`_ for the detailed documentation.
