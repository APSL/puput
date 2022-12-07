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
        'wagtail.contrib.legacy.richtext',
        'wagtail.core',
        'wagtail.admin',
        'wagtail.documents',
        'wagtail.snippets',
        'wagtail.users',
        'wagtail.images',
        'wagtail.embeds',
        'wagtail.search',
        'wagtail.sites',
        'wagtail.contrib.redirects',
        'wagtail.contrib.forms',
        'wagtail.contrib.sitemaps',
        'wagtail.contrib.routable_page',
        'taggit',
        'modelcluster',
        'django_social_share',
        'puput',
    )


3. Add Wagtail's required middleware classes to :code:`MIDDLEWARE_CLASSES` in your Django settings.

.. code-block:: python

    MIDDLEWARE_CLASSES = (
        ...
        'wagtail.contrib.redirects.middleware.RedirectMiddleware',
    )

4. Add the :code:`request` context processor to the :code:`TEMPLATE_CONTEXT_PROCESSORS` structure in your Django settings.

.. code-block:: python

    TEMPLATE_CONTEXT_PROCESSORS = (
        ...
        'django.template.context_processors.request',
    )

5. Set the :code:`WAGTAIL_SITE_NAME` variable to the name of your site in your Django settings.

.. code-block:: python

    WAGTAIL_SITE_NAME = 'Puput blog'

6. Set the :code:`WAGTAILADMIN_BASE_URL` variable to the base url of your site in your Django settings.

.. code-block:: python

    WAGTAILADMIN_BASE_URL = 'http://localhost:8000/'

7. Configure the :code:`MEDIA_ROOT` and :code:`MEDIA_URL` settings as described in the `Wagtail Docs <http://docs.wagtail.io/en/v1.1/advanced_topics/settings.html#ready-to-use-example-configuration-files>`_.

.. code-block:: python

    MEDIA_ROOT = os.path.join(PROJECT_ROOT, 'media')
    MEDIA_URL = '/media/'


8. Place Puput's URLs at the **bottom** of the urlpatterns. It also includes Wagtail's URLs.

.. code-block:: python

    urlpatterns = [
        ...
        path(r'', include('puput.urls')),
    ]

9. To make your Django project serve your media files (e.g. things you upload via the admin) during development, don't forget to add this to your urlpatterns:

.. code-block:: python


    from django.conf import settings
    from django.conf.urls import url

    if settings.DEBUG:
        import os
        from django.conf.urls.static import static
        from django.contrib.staticfiles.urls import staticfiles_urlpatterns
        from django.views.generic.base import RedirectView

        urlpatterns += staticfiles_urlpatterns() # tell gunicorn where static files are in dev mode
        urlpatterns += static(settings.MEDIA_URL + 'images/', document_root=os.path.join(settings.MEDIA_ROOT, 'images'))
        urlpatterns += [
            path(r'favicon\.ico', RedirectView.as_view(url=settings.STATIC_URL + 'myapp/images/favicon.ico')),
        ]


10. Run :code:`python manage.py migrate` and :code:`python manage.py puput_initial_data` to load initial data to start a blog site.
11. Open your browser at http://127.0.0.1:8000/blog/ to view your blog home page. Go to http://127.0.0.1:8000/blog_admin/ to view the admin site and edit your content.

.. _wagtail_app:

Installation on top of Wagtail
------------------------------
0. This assumes that you have Wagtail >= 2.0 installed and you can access /admin; if this is not the case or you would like to use a newer version of Wagtail than is in the dependencies of puput, follow the steps below in a python venv:

.. code-block:: bash

    pip install --upgrade pip
    pip install wheel
    pip install wagtail django-colorful django-el-pagination django-social-share
    pip install --no-deps puput
    wagtail start mysite
    cd mysite
    python manage.py migrate
    python manage.py createsuperuser

1. If you haven't already, install Puput and its dependencies via :code:`pip install puput`.
2. In your Django settings (most commonly settings/base.py inside the wagtail directory), add the following to the :code:`INSTALLED_APPS` following the wagtail section:

.. code-block:: python
 
     'wagtail.contrib.sitemaps',
     'wagtail.contrib.routable_page',
     'django_social_share',
     'puput',
     'colorful',

3. In the same file, also add the line :code:`PUPUT_AS_PLUGIN = True` to the very bottom

4. In the same folder, add to :code:`urls.py` near the top :code:`from puput import urls as puput_urls` and just above :code:`url(r'', include(wagtail_urls)),` add :code:`url(r'',include(puput_urls)),`

5. Run :code:`python manage.py migrate` followed by :code:`python manage.py runserver 0:8000` to start the server

6. To create a Puput blog navigate to the Wagtail admin interface at :code:`127.0.0.1:8000/admin` and create a new child page of type :code:`Blog`. Every blog post is then created as a child of this blog.

Docker
------
If you want to run Puput in a Docker container please visit `docker-puput  <https://github.com/APSL/docker-puput/>`_
for detailed instructions.
