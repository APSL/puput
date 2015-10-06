Import your blog data
=====================

If you need to migrate a blog system to Puput we provide you a various tools to import your data.

Zinnia
------
1. Install zinnia-to-puput package and its dependencies :code:`pip install zinnia-to-puput`
2. Add `zinnia2puput` to your :code:`INSTALLED_APPS` in :file:`settings.py` file.
3. Run the management command::

    python manage.py zinnia2import

You can optionally pass the slug and the title of the blog to the importer::

    python manage.py zinnia2import --slug=blog --title="Puput blog"

Wordpress
---------
TODO
