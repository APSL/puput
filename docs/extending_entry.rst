Extending Entry Page
====================

Puput allows extend the :class:`EntryPage` model. It provides two approaches to extend entries depending on the project
requirements.

Multi-table inheritance
-----------------------
The easiest way to extend :class:`EntryPage` model is using `multi-table inheritance <https://docs.djangoproject.com/en/dev/topics/db/models/#multi-table-inheritance>`_.
Imagine if you need an special entry that needs a mandatory video url. You can write an entry model like
this on :file:`models.py` of your project:

.. code-block:: python

    from django.db import models
    from puput.models import EntryPage


    class VideoEntryPage(EntryPage):
        video_url = models.URLField()
        content_panels = EntryPage.content_panels + [
            FieldPanel('video_url')
        ]

You also need to modify ``subpage_types`` field of :class:`BlogPage` model as by default is bounded
to have only :class:`EntryPage` as children. You can rewrite the above example with this:

.. code-block:: python

    from django.db import models
    from puput.models import EntryPage, BlogPage


    class VideoEntryPage(EntryPage):
        video_url = models.URLField()
        content_panels = EntryPage.content_panels + [
            FieldPanel('video_url')
        ]
    BlogPage.subpage_types.append(VideoEntryPage)

This will create two independent tables on the database so you can create entries on your blog that are instances
of :class:`EntryPage` or :class:`VideoEntryPage`.

Abstract base classes
---------------------
Another approach to have an extension of entries is using `abstract base classes <https://docs.djangoproject.com/en/dev/topics/db/models/#abstract-base-classes>`_
inheritance method by inheriting from :class:`EntryAbstract` instead of :class:`EntryPage`.
In the previous example, it's shown a blog with regular entries (:class:`EntryPage`) and tv entries (:class:`VideoEntryPage`).
If you only want to have :class:`VideoEntryPage` on your blog and create a simple table you need to extend
:class:`EntryAbstract` model on :file:`models.py` of your project.

.. code-block:: python

    from django.db import models
    from puput.abstracts import EntryAbstract
    from wagtail.wagtailadmin.edit_handlers import FieldPanel


    class VideoEntryAbstract(EntryAbstract):
        video_url = models.URLField()
        
        content_panels = EntryAbstract.content_panels + [
            FieldPanel('video_url')
        ]

        class Meta:
            abstract = True

.. warning::
    Do not import the :class:`EntryPage` model in your :file:`models.py` where defining the abstract extended model
    because it will cause a circular importation.

Registering entry extension
~~~~~~~~~~~~~~~~~~~~~~~~~~~
You have to register the model extension in :file:`settings.py` adding :code:`PUPUT_ENTRY_MODEL` with the path of the abstract model.

Following the previous example you have to add :code:`PUPUT_ENTRY_MODEL` in your :file:`settings.py` file:

.. code-block:: python

    PUPUT_ENTRY_MODEL = 'youproject.models.VideoEntryAbstract'

Migrations
~~~~~~~~~~
If you extend :class:`EntryPage` model you must migrate the database in order to the see the changes
that you made on the model. However if you perform a ``makemigrations`` operation it will create a migration in
:class:`puput.migrations` of your local Puput module folder.

So you need to define a new path to store the changes made on :class:`EntryPage` model extension. You have to use  :code:`MIGRATION_MODULES` for this purpose:

.. code-block:: python

    MIGRATION_MODULES = {'puput': 'youproject.puput_migrations'}

After run ``makemigrations puput`` migrations will appear on ``puput_migrations`` folder.

.. note::
    It’s recommended that the new initial migration represents the initial Puput migration in order to avoid conflicts
    when applying ``migrate puput`` command. A recommend way is run ``makemigrations puput`` **before** define Entry model
    extension on :file:`settings.py` by setting :code:`PUPUT_ENTRY_MODEL`.
