.. image:: https://readthedocs.org/projects/puput/badge/?version=latest
    :target: https://readthedocs.org/projects/puput/?badge=latest
    :alt: Documentation Status

Puput
=====

Puput is a powerful and simple Django app to manage a blog. It uses the awesome Wagtail CMS as content management system.

Puput is the catalan name for `Hoopoe <https://en.wikipedia.org/wiki/Hoopoe>`_ which is indeed a beautiful bird.

.. image:: http://i.imgur.com/ndZLeWb.png

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

Setup
~~~~~

If you have a running Django project and you want to add blog site to your project,
please follow **Standalone blog app** steps. Otherwise follow the **Wagtail blog app** steps if you are currently using Wagtail on your project.


Standalone blog app
-------------------
1. Install Puput and its dependencies :code:`pip install puput`

2. Add to :code:`PUPUT_APPS` to your :code:`INSTALLED_APPS` in :code:`settings.py` file.

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

5. Set :code:`WAGTAIL_SITE_NAME` variable in :code:`settings.py` file with your site name
6. Place Puput urls at the **bottom** of the urlpatterns. It also includes Wagtail urls.

.. code-block:: python

    urlpatterns = [
        ...
        url(r'', include('puput.urls')),
    ]
7. Run :code:`python manage.py migrate` and :code:`python manage.py puput_initial_data` to load initial data to start a blog site.
8. Open your broswer at http://127.0.0.1:8000/blog/ to view your blog home page.


Wagtail blog app
----------------
1. Install Puput and its dependencies :code:`pip install puput`
2. Add :code:`puput` to your :code:`INSTALLED_APPS` in :code:`settings.py` file.
3. If you have previously defined Wagtail urls in :code:`urls.py` set :code:`PUPUT_AS_PLUGIN = True` in the :code:`settings.py`. This will avoid to include Wagtail urls again when you include necessary Puput urls.
4. Include Puput urls in your :code:`urls.py` file.

.. code-block:: python

    urlpatterns = [
        ...
        url(r'', include('puput.urls')),
        ...
    ]

5. Run :code:`python manage.py migrate`

Documentation
~~~~~~~~~~~~~
Visit `Puput documentation <http://puput.readthedocs.org>`_ for the detailed documentation.
