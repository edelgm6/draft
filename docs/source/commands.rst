========
Commands
========

.. module:: draft.cli

Draft commands can be split into three buckets:

1. **Create** a project
2. **Format** a project's file content
3. **Maintain** a project

Create
------
.. autofunction:: create_project(title)
.. autofunction:: parse(filepath)

Format
------

.. autofunction:: split(filename)
.. autofunction:: trim(filename)

Maintain
--------

.. autofunction:: sequence()
.. autofunction:: stats()
.. autofunction:: compile()
.. autofunction:: outline()
