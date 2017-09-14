Setup
=====

If you're starting from a Django project without Wagtail integration and you want to add a blog site to your project,
please follow the steps outlined under :ref:`standalone_app`. If you are already using Wagtail, refer to :ref:`wagtail_app`.

.. _standalone_app:

Standalone blog app
-------------------
1. Install Puput and its dependencies via :code:`pip install puput`.

2. Append :code:`PUPUT_APPS` to :code:`INSTALLED_APPS` in your settings.

.. code-block:: python

    from puput import PUPUT_APPS

    INSTALLED_APPS += PUPUT_APPS

This includes Puput, `Wagtail's apps <http://docs.wagtail.io/en/v1.0/advanced_topics/settings.html#wagtail-apps>`_ and certain `third-party dependencies <http://docs.wagtail.io/en/v1.0/advanced_topics/settings.html#third-party-apps>`_.
If you are already referencing one of these apps in your :code:`INSTALLED_APPS` list, please include the following apps manually in order to avoid app collisions:

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
        'taggit',
        'modelcluster',
        'puput',
    )


3. Add Wagtail's required middleware classes to :code:`MIDDLEWARE_CLASSES` in your Django settings.

.. code-block:: python

    MIDDLEWARE_CLASSES = (
        ...
        'wagtail.wagtailcore.middleware.SiteMiddleware',
        'wagtail.wagtailredirects.middleware.RedirectMiddleware',
    )

4. Add the :code:`request` context processor to the :code:`TEMPLATE_CONTEXT_PROCESSORS` structure in your Django settings.

.. code-block:: python

    TEMPLATE_CONTEXT_PROCESSORS = (
        ...
        'django.core.context_processors.request',
    )

5. Set the :code:`WAGTAIL_SITE_NAME` variable to the name of your site in your Django settings.

.. code-block:: python

    WAGTAIL_SITE_NAME = 'Puput blog'

6. Configure the :code:`MEDIA_ROOT` and :code:`MEDIA_URL` settings as described in the `Wagtail Docs <http://docs.wagtail.io/en/v1.1/advanced_topics/settings.html#ready-to-use-example-configuration-files>`_.

.. code-block:: python

    MEDIA_ROOT = os.path.join(PROJECT_ROOT, 'media')
    MEDIA_URL = '/media/'


7. Place Puput's URLs at the **bottom** of the urlpatterns. It also includes Wagtail's URLs.

.. code-block:: python

    urlpatterns = [
        ...
        url(r'', include('puput.urls')),
    ]

8. To make your Django project serve your media files (e.g. things you upload via the admin) during development, don't forget to add this to your urlpatterns:

.. code-block:: python


    from django.conf import settings

    if settings.DEBUG:
        import os
        from django.conf.urls.static import static
        from django.views.generic.base import RedirectView
        from django.contrib.staticfiles.urls import staticfiles_urlpatterns

        urlpatterns += staticfiles_urlpatterns() # tell gunicorn where static files are in dev mode
        urlpatterns += static(settings.MEDIA_URL + 'images/', document_root=os.path.join(settings.MEDIA_ROOT, 'images'))
        urlpatterns += [
            (r'^favicon\.ico$', RedirectView.as_view(url=settings.STATIC_URL + 'myapp/images/favicon.ico')),
        ]


9. Run :code:`python manage.py migrate` and :code:`python manage.py puput_initial_data` to load initial data to start a blog site.
10. Open your browser at http://127.0.0.1:8000/blog/ to view your blog home page. Go to http://127.0.0.1:8000/blog_admin/ to view the admin site and edit your content.

.. _wagtail_app:

Installation on top of Wagtail
------------------------------
1. Install Puput and its dependencies via :code:`pip install puput`.
2. Add :code:`puput`, :code:`wagtail.contrib.wagtailsitemaps` and :code:`wagtail.contrib.wagtailroutablepage` to :code:`INSTALLED_APPS` in your Django settings.
3. If you have previously defined Wagtail URLs in your patterns, set the :code:`PUPUT_AS_PLUGIN` setting to :code:`True`. This will avoid duplicate inclusion of Wagtail's URLs when you include Puput's URLs.
4. Include Puput's URLs in your patterns **before** Wagtail's URLs.

.. code-block:: python

    urlpatterns = [
        ...
        url(r'', include('puput.urls')),
        url(r'', include(wagtail_urls)),
    ]

5. Run :code:`python manage.py migrate`.


Docker
------
If you want to run Puput in a Docker container please visit `docker-puput  <https://github.com/APSL/docker-puput/>`_
for detailed instructions.
