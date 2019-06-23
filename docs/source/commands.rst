========
Commands
========

.. module:: draft.cli

Using Draft's commands is easy.
In your terminal just use ``draft COMMAND``.
If you ever need additional help while using the tool, just use ``draft --help`` or ``draft COMMAND --help`` to get information on specific commands.

Commands can be broken out into three buckets:

1. **Create** a project
2. **Format** a project's file content
3. **Maintain** a project

Create
------
Create commands are helpful when first starting up a project (``parse`` especially for legacy projects).

.. autofunction:: create_project(title)

  Example file tree:

  .. include:: start-file-tree.rst

.. autofunction:: parse(filename)

Format
------
Format commands are used to change the way text is arranged within files.

.. autofunction:: split(filename=None)
.. autofunction:: trim(filename=None)

Maintain
--------
Maintain commands are used mostly as you are writing, organizing, and publishing your project.

.. autofunction:: sequence()
.. note::
  The number of digits in each file/folder *sequence* is governed by the total number of items at that *level.*
  For example, if you have 5 sections and 150 scenes, your sections will sequence 1, 2, 3, 4, 5 and your scenes will sequence 001, 002, 003, etc.

.. autofunction:: stats()
.. autofunction:: compile()
.. autofunction:: outline()
