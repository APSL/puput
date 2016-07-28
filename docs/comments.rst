Comments
========

Puput allows customize the comment system for your blog entries. Simply go to settings tab while editing blog properties
and add the required parameters depending on which system you want to use.

Disqus
------
Set *Disqus api secret* and *Disqus shortname* with your project values and comments will be displayed in each blog entry.
*Disqus api secret* is needed to retrieve the number of comments of each entry. If you don't need such data
in your blog just fill *Disqus shortname* field.

.. note::

    If you set *Disqus api secret* you need to install `tapioca-disqus` to access to the Disqus API ::

        pip install tapioca-disqus
