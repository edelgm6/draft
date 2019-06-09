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
Let's assume you wanted to create a project titled "Catcher In the Rye."

1. Create project folder: ``mkdir catcher``
2. Create virtualenv: ``virtualenv rye``
3. Activate virtualenv: ``source rye/bin/activate``
4. Install Draft: ``pip install draft-cli``
5. Create project: ``draft create-project 'Catcher In the Rye'``

You will now have the following file tree::

    Catcher In the Rye/
    └─project/
    │ └─Catcher In the Rye/
    │     01-Scene 1.md
    └─.gitignore

From a WIP Project
------------------

1. Follow the same steps as "Starting From Scratch."

2. Take your current project in whatever format it is in, and paste it into a Markdown file (e.g., ``myproject.md``) in your root. Your project should now look like this::

    Catcher In the Rye/
    └─project/
    │ └─Catcher In the Rye/
    │     01-Scene 1.md
    └─myproject.md
    └─.gitignore

3. Edit your file's Headings to follow Markdown conventions. This will inform your file tree:

  - ## for each Section (e.g., ## Introduction)

  - ### for each Chapter

  - #### for each Sub-chapter

  - ##### for each Scene

  For example, your ``myproject.md`` file might look like this:

    # Catcher In the Rye

    ## Meeting Holden

    ### Leaving School

    #### Roommates

    ##### We Meet Holden

    If you really want to hear about it, the first thing you'll probably want to know is where I was born, and what my lousy childhood was like, and how my parents were occupied and all before they had me, and all that David Copperfield kind of crap, but I don't feel like going into it, if you want to know the truth.

    **Note: You can mix and match headings as needed (or not use them at all) -- the only requirements are the Scenes.**


4. Run ``draft parse myproject.md`` which will take your file and split it into Section, Chapter, and Sub-Chapter *folders* and Scene Markdown files.

  E.g., the above ``myproject.md`` would result in::

    Catcher In the Rye/
    └─project/
    │ └─Catcher In the Rye/
    │   └─01-Meeting Holden
    │     └─01-Leaving School
    │       └─01-Roommates
    │         └─01-We Meet Holden.md
    └─myproject.md
    └─.gitignore

  If it doesn't turn out exactly as you want, no biggie!
  ``myproject.md`` is preserved, so just make whatever tweaks you need and re-run ``draft parse myproject.md`` to update the tree.
