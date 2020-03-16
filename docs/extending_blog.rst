Extending Blog Page
====================

Puput allows you to extend the :class:`BlogPage` model depending on the project requirements.

Abstract base classes
---------------------
In order to extend blog page use `abstract base classes <https://docs.djangoproject.com/en/dev/topics/db/models/#abstract-base-classes>`_
inheritance method by inheriting from :class:`BlogAbstract` instead of :class:`BlogPage`.
Sometimes you may need to define additional informations specific to your entire blog page i.e. social media links.
To be able to use them, first you need to extend :class:`BlogAbstract` model on :file:`models.py` of your project.

.. code-block:: python

    from django.db import models
    from django.utils.translation import ugettext_lazy as _

    from wagtail.wagtailadmin.edit_handlers import FieldPanel, MultiFieldPanel

    from puput.abstracts import BlogAbstract


    class MyBlogAbstract(BlogAbstract):
        facebook_url = models.URLField(blank=True)
        instagram_url = models.URLField(blank=True)
        pinterest_url = models.URLField(blank=True)

        settings_panels = BlogAbstract.settings_panels + [MultiFieldPanel([
                FieldPanel('facebook_url'),
                FieldPanel('instagram_url'),
                FieldPanel('pinterest_url'),
            ], heading=_("Socials"))]

        class Meta:
            abstract = True

.. warning::
    Do not import the :class:`BlogPage` model in your :file:`models.py` where defining the abstract extended model
    because it will cause a circular importation.

Registering blog extension
~~~~~~~~~~~~~~~~~~~~~~~~~~~
You have to register the model extension in :file:`settings.py` adding :code:`PUPUT_BLOG_MODEL` with the path of the abstract model.

Following the previous example you have to add :code:`PUPUT_BLOG_MODEL` in your :file:`settings.py` file:

.. code-block:: python

    PUPUT_BLOG_MODEL = 'app_name.models.BlogAbstract'

Migrations
~~~~~~~~~~
If you extend :class:`BlogPage` model you must migrate the database in order to the see the changes
that you made on the model. However if you perform a ``./manage.py makemigrations`` operation it will create a migration in
:class:`puput.migrations` of your local Puput module folder.

So you need to define a new path to store the changes made on :class:`BlogPage` model extension. You have to use  :code:`MIGRATION_MODULES` for this purpose:

.. code-block:: python

    MIGRATION_MODULES = {'puput': 'app_name.puput_migrations'}

After run ``./manage.py makemigrations puput`` migrations will appear on ``app_name.puput_migrations`` folder.

.. note::
    It’s recommended that the new initial migration represents the initial Puput migration in order to avoid conflicts
    when applying ``./manage.py migrate puput`` command. A recommend way is run ``./manage.py makemigrations puput`` **before** define Blog model
    extension on :file:`settings.py` by setting :code:`PUPUT_BLOG_MODEL`.