Comments
========

Puput allows customize the comment system for your blog entries. Simply go to settings tab while editing blog properties
and add the required parameters depending on which system you want to use.

There is a :code:`PUPUT_COMMENTS_PROVIDER` setting that should point to the specific provider class. It defaults to :class:`DisqusCommentsProvider`.

Disqus
------
Set *Disqus api secret* and *Disqus shortname* with your project values and comments will be displayed in each blog entry.
*Disqus api secret* is needed to retrieve the number of comments of each entry. If you don't need such data
in your blog just fill *Disqus shortname* field.

In your :file:`settings.py` file:

.. code-block:: python

    PUPUT_COMMENTS_PROVIDER = 'puput.comments.DisqusCommentsProvider'


.. note::

    If you set *Disqus api secret* you need to install `tapioca-disqus` to access to the Disqus API ::

        pip install tapioca-disqus


Django Comments
---------------

Use django comments if you want to store comments in your own database and be able to access them as django models.

In your :file:`settings.py` file:

.. code-block:: python

    PUPUT_COMMENTS_PROVIDER = 'puput.comments.DjangoCommentsProvider'


.. note::

    To use django comments you need to install either::

        pip install django-contrib-comments

    and optionally for features like comment threads, email confirmations, notifications etc::

        pip install django-comments-xtd

Customize comment template
--------------------------

To change how comments are displayed, subclass the provider class you're using and change its :code:`template`
method to return the path to your custom template.

Implement your own provider
---------------------------

To add your own comment provider you will need to subclass :class:`CommentsProvider` and implement its methods:

  :code:`template`

return the path to the template used to render the comment section

 :code:`get_context`

return dictionary with data needed in your template

 :code:`get_num_comments`

return number of comments for the entry page
