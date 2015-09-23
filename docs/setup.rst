Setup
=====

If you have a running Django project and you want to add blog site to your project,
please follow :ref:`standalone_app` steps. Otherwise follow the :ref:`wagtail_app` steps if you are currently using Wagtail on your project.

.. _standalone_app:

Standalone blog app
-------------------
1. Install Puput and its dependencies :code:`pip install puput`

2. Add to :code:`PUPUT_APPS` to your :code:`INSTALLED_APPS` in :file:`settings.py` file.

.. code-block:: python

    from puput import PUPUT_APPS

    INSTALLED_APPS += PUPUT_APPS

This includes Puput app, `Wagtail apps <http://docs.wagtail.io/en/v1.0/advanced_topics/settings.html#wagtail-apps>`_ and `Third party apps <http://docs.wagtail.io/en/v1.0/advanced_topics/settings.html#third-party-apps>`_.
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


3. Add Wagtail required middleware classes in :file:`settings.py` file

.. code-block:: python

    MIDDLEWARE_CLASSES = (
        ...
        'wagtail.wagtailcore.middleware.SiteMiddleware',
        'wagtail.wagtailredirects.middleware.RedirectMiddleware',
    )

4. Add :code:`request` context processor to :code:`TEMPLATE_CONTEXT_PROCESSORS` structure in :file:`settings.py` file

.. code-block:: python

    TEMPLATE_CONTEXT_PROCESSORS = (
        ...
        'django.core.context_processors.request',
    )

5. Set :code:`WAGTAIL_SITE_NAME` variable in :file:`settings.py` file with your site name
6. Place Puput urls at the **bottom** of the urlpatterns. It also includes Wagtail urls.

.. code-block:: python

    urlpatterns = [
        ...
        url(r'', include('puput.urls')),
    ]
7. Run :code:`python manage.py migrate` and :code:`python manage.py puput_initial_data` to load initial data to start a blog site.
8. Open your broswer at http://127.0.0.1:8000/blog/ to view your blog home page.


.. _wagtail_app:

Wagtail blog app
----------------
1. Install Puput and its dependencies :code:`pip install puput`
2. Add :code:`puput` to your :code:`INSTALLED_APPS` in :file:`settings.py` file.
3. If you have previously defined Wagtail urls in :file:`urls.py` set :code:`PUPUT_AS_PLUGIN = True` in the :file:`settings.py`. This will avoid to include Wagtail urls again when you include necessary Puput urls.
4. Include Puput urls in your :file:`urls.py` file.

.. code-block:: python

    urlpatterns = [
        ...
        url(r'', include('puput.urls')),
        ...
    ]

5. Run :code:`python manage.py migrate`