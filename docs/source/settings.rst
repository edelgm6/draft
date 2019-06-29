========
Settings
========

Overview
--------

You can configure your project's settings with the ``settings.yml`` file in your project's root (note: this is automatically added for you with the ``generate-project`` command).

A few things to note before getting into the specifics:

  The ``settings.yml`` is not required -- if you want to keep the default options, you can just delete it

  None of the *individual* settings in ``settings.yml`` are required. Omitting a setting will just use the default value

settings.yml
------------

The default file layout (i.e., the one added automatically with ``generate-project``) is below. Settings are split into four groups:

.. code-block:: yaml

  headers:
    section: true
    chapter: true
    sub_chapter: true

  warnings:
    parse: true
    split: true
    sequence: true
    trim: true

  overrides:

  author:

headers
~~~~~~~

**headers** defines whether or not each header type is displayed when using the ``compile`` feature.

This is useful for when you want to use the *organization* of the file structure without it affecting your *final product* (e.g., I might want to split my chapters up into sections to help keep track of them, but not present those sections to the reader).

warnings
~~~~~~~~

**warnings** allows you to enable/disable the warning messages that come up during commands that affect the content of your files.

overrides
~~~~~~~~~

**overrides** is used to override the Section, Chapter, or Sub-Chapter name during the ``compile`` command.

For example, if we use the ``parse`` command, the chapter name *Ahab's Leg* would be translated into a folder *Ahabs Leg* -- note the lack of an apostrophe. When using the ``compile`` command, we would want to add that apostrophe back in. To do so, the ``settings.yml`` might look like:

.. code-block:: yaml

  overrides:
    Ahabs Leg: Ahab's Leg

.. note::
  When using the ``parse`` command, any header names that require cleaning before being created will automatically be logged in the ``settings.yml`` file if it exists (i.e., the above example would have been added automatically if detected during ``parse``)

author
~~~~~~

**author** is used to add an author name during the ``compile`` command.
