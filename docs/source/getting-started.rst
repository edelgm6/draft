===============
Getting Started
===============

Prerequisites
-------------
- Python 3 (required)
- Git (not required, but recommended)
- Virtualenv (not required, but recommended)

Starting From Scratch
---------------------
Creating a new project from scratch is easy.
Let's assume you wanted to create a project titled *Catcher In the Rye.*

1. Create project folder: ``mkdir catcher``
2. Create virtualenv: ``virtualenv rye``
3. Activate virtualenv: ``source rye/bin/activate``
4. Install Draft: ``pip install draft-cli``
5. Create project: ``draft create-project 'Catcher In The Rye'``

You will now have the following file tree (note that Draft truncates your root directory to ``catcher-rye/``):

.. include:: start-file-tree.rst

From a WIP Project
------------------

1. Follow the same steps as "Starting From Scratch."

2. Take your current project in whatever format it is in, and paste it into a Markdown file and put in your project's root directory (e.g., if your current project is ``myproject.md``, you should put it in ``catcher-rye/``, in the same folder as ``project/``).

3. Edit your file's Headings to follow Markdown conventions. This will inform your file tree:

  - # for the Title (e.g., # Catcher In The Rye)

  - ## for each Section

  - ### for each Chapter

  - #### for each Sub-chapter

  - ##### for each Scene

  For example, your ``myproject.md`` file might look like this:

    # Catcher In The Rye

    ## Meeting Holden

    ### Leaving School

    #### Roommates

    ##### We Meet Holden

    If you really want to hear about it, the first thing you'll probably want to know is where I was born, and what my lousy childhood was like, and how my parents were occupied and all before they had me, and all that David Copperfield kind of crap, but I don't feel like going into it, if you want to know the truth.

.. note::
  You can mix and match headings as needed (or not use them at all) -- but *scene* headers are needed if you want to split into multiple files


4. Run ``draft parse myproject.md`` which will take your file and split it into Section, Chapter, and Sub-Chapter *folders* and Scene Markdown files.

  E.g., the above ``myproject.md`` would result in::

    catcher-rye/
    └─project/
    │ └─Catcher In The Rye/
    │   └─1-Meeting Holden
    │     └─1-Leaving School
    │       └─1-Roommates
    │         └─1-We Meet Holden.md
    └─myproject.md
    └─settings.yml
    └─.gitignore

  If it doesn't turn out exactly as you want, no biggie!
  ``myproject.md`` is preserved, so just make whatever tweaks you need and re-run ``draft parse myproject.md`` to update the tree.
