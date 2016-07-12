Settings
========

Puput provides setting variables in order to customize your installation.

.. setting:: PUPUT_ENTRY_MODEL

PUPUT_ENTRY_MODEL
-----------------
**Default value:** ``'puput.abstracts.EntryAbstract'`` (Empty string)

String setting to define the base model path for Entry model. See :doc:`extending` for more details.

.. setting:: PUPUT_AS_PLUGIN

PUPUT_AS_PLUGIN
---------------
**Default value:** ``False`` (Empty string)

Boolean setting to define if you set Puput as a plugin of a previously configured Wagtail project.

.. setting:: PUPUT_USERNAME_FIELD

PUPUT_USERNAME_FIELD
--------------------
**Default value:** ``'username'`` (Empty string)

String setting to define the default author username field. Useful for people that are using a custom User model and/or
other authentication method where an username is not mandatory.

PUPUT_USERNAME_REGEX
--------------------
**Default value:** ``'\w+'`` (Empty string)

String setting to define the default author username regex used in routes. Useful for people that are using a custom
User model.