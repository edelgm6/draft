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

.. autofunction:: parse(filepath)

Format
------
Format commands are used to change the way text is arranged within files.

.. autofunction:: split(filepath=None)
.. autofunction:: trim(filepath=None)

Maintain
--------
Maintain commands are used mostly as you are writing, organizing, and publishing your project.

.. autofunction:: sequence()
.. autofunction:: stats()
.. autofunction:: compile()
.. autofunction:: outline()
