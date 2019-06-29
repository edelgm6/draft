========
Examples
========
The ``examples/`` directory contains Markdown files that demonstrate Draft commands.

Getting Started
---------------

1. Create a new project: ``draft create-project 'New Project'``
2. Navigate to the project's root directory: ``cd new-project``
3. Download the ``examples/`` folder into the ``new-project/`` directory: ``svn checkout https://github.com/edelgm6/draft/trunk/examples``
4. Copy all of the files in ``examples/`` into your ``new-project/`` root directory

Trying the Commands
-------------------

.. _parse:

parse, stats, outline, and compile
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

parse
*****

``parse.md`` contains the first chapters of *Moby Dick* and can be used to build out a starter file tree.

1. Ensure your terminal is navigated to ``new-project/`` root directory and that ``parse.md`` is in the same folder
2. Run ``draft parse parse.md``


You should now find a starting file tree based on the contents of ``parse.md`` in the ``project/`` folder.

stats
*****

3. Run ``draft stats``

You'll now have a printout of the word count, section count, chapter count, and sub-chapter count

outline
*******

4. Run ``draft outline``

This creates ``outline.md`` which is a Markdown file showing the basic outline of your story.

compile
*******

5. Run ``draft compile``

This compiles your entire project into a single Markdown file, `Moby Dick.md`.

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

``sequence/`` contains a project, ``Moby Dick or The Whale/`` that has out of sequence files:
- ``Call Me Ishmael.md`` and ``Manhattoes.md`` both have the same sequence of ``1``
- There is no ``2`` sequence

To show how the ``draft sequence`` command fixes this:

1. Make sure your ``project/`` folder is completely empty
2. Move ``sequence/`` *into* the project folder
3. Run ``draft sequence``

You will be prompted to choose *which of the 1 indexed files should go first*.
Whichever you choose will become the new `1` sequence and the other will be come the `2` sequence.
