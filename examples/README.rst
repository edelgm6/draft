========
Examples
========
The ``examples/`` directory contains Markdown files that demonstrate Draft commands.

Getting Started
---------------

1. Create a new project: ``draft create-project 'New Project'``
2. Navigate to the project's root directory: ``cd new-project``
3. Download the ``examples/`` files into the ``new-project`` directory

Trying the Commands
-------------------

.. _parse:

parse, stats, compile, and outline
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

``parse.md`` contains the first chapters of *Moby Dick* and can be used to build out a starter file tree.

1. Ensure your terminal is navigated to the same folder containing ``parse.md``
2. Run ``draft parse parse.md``
3. Run ``draft stats``

You should now find a starting file tree based on the contents of ``parse.md`` in the ``project/`` folder and a printout of the summary statistics of the project.

split
~~~~~

``split.md`` contains a paragraph from **Moby Dick** where **each paragraph takes up a single line.**
To make writing and change tracking in Git easier, we want to use ``draft split`` to put each sentence on its own line.

1. Ensure your terminal is navigated to the same folder containing ``split.md``
2. Run ``draft split split.md``

``split.md`` will now have each of its sentences on a discrete line.

If you've already tried the :ref:`parse` example, you can run ``draft split`` to act on every file across the entire ``project/`` folder.

sequence
~~~~~~~~

``sequence/`` contains folders and Markdown files that have *duplicate indexes**.
You can use ``draft sequence`` to re-sequence the files into a clean index.

1. Make sure your ``project/`` folder is completely empty
2. Move ``sequence/`` *into* the project folder
3. Run ``draft sequence``
