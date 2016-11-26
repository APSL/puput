Import your blog data
=====================

If you need to migrate a blog system to Puput we provide you a various tools to import your data.

Zinnia
------
1. Install zinnia-to-puput package and its dependencies :code:`pip install zinnia-to-puput`
2. Add `zinnia2puput` to your :code:`INSTALLED_APPS` in :file:`settings.py` file.
3. Run the management command::

    python manage.py zinnia2puput

You can optionally pass the slug and the title of the blog to the importer::

    python manage.py zinnia2puput --slug=blog --title="Puput blog"

Wordpress
---------
1. Ensure the libxml and libxslt prerequisites are installed.

On Ubuntu::

    sudo apt-get install libxml2-dev libxslt-dev

On CentOS or Red Hat::

    sudo yum install libxml2-devel libxml++-devel libxslt-devel

2. Install wordpress-to-puput package and its dependencies :code:`pip install wordpress-to-puput`
3. Add :code:`wordpress2puput` to your :code:`INSTALLED_APPS` in :code:`settings.py` file.
4. Run the management command::

    python manage.py wp2puput path_to_wordpress_export.xml

You can optionally pass the slug and the title of the blog to the importer::

    python manage.py wp2puput path_to_wordpress_export.xml --slug=blog --title="Puput blog"

Blogger
-------
1. Install blogger2puput package and its dependencies :code:`pip install blogger2puput`
2. Add :code:`blogger2puput` to your :code:`INSTALLED_APPS` in :code:`settings.py` file.
3. Run the management command::

    python manage.py blogger2puput --blogger_blog_id=Your BlogID --blogger_api_key=Your APIKey

You can optionally pass the slug and the title of the blog to the importer::

    python manage.py blogger2puput --slug=blog --title="Puput blog" --blogger_blog_id=Your BlogID --blogger_api_key=Your APIKey
