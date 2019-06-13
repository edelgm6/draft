====================
Draft Writing System
====================

When you're writing something short, a Google Doc or Word file works great.
But get beyond a few thousand words and all of a sudden opening that file comes with a sense of dread.

Philosophy
----------

1) Writing in *modules* (or 'scenes' in Draft lingo) is easier and more fun than working out of a single large document.

2) Writing in plaintext is a more pure and distraction-free experience than `WYSIWYG <https://en.wikipedia.org/wiki/WYSIWYG>`_ word processors.

3) Git is too useful a tool to not use in a writing project.

Organization
------------

Folders
~~~~~~~

A Draft project is made up of a simple file tree as shown below::

    whalebook/
    └─project/                                   Organization:
    │ └──Moby Dick, Or The Whale/                [Title]
    │    └──01-Nantucket/                        [Section 1]
    │    │  └──01-Meeting Ishmael/               [Chapt 1]
    │    │  │  └──01-Loomings/                   [Sub-Chapt 1]
    │    │  │  │    01-His Name is Ishmael.md    [Scene 1]
    │    │  │  │    02-Habit of Going To Sea.md  [Scene 2]
    │    │  │  └──02-The Carpet-Bag/             [Sub-Chapter 2]
    │    │  │  │    03-Old Manhatto.md           [Scene 3]
    │    │  │  │    etc.
    │    │  │  └──03-etc.
    │    │  └─02-Shoving Off/                    [Chapter 2]
    │    │      etc.
    │    └──02-Whaling/                          [Section 2]
    │         etc.
    └─settings.yml

You don't *need* to use every 'level' of the project -- i.e., you could just have the Title and a bunch of scenes, only use sections and scenes, have some scenes in sub-chapters and some scenes in chapters, etc.

The only required elements are the `project/` folder, the `title/` folder, and scene `.md` files.

Sequencing
~~~~~~~~~~

Prepend ``01-``, ``02-``, etc. to your folders and files to keep them cleanly sequenced.

As you get to have a lot of folders and files, *re-sequencing* can get to be a pain (e.g., if you have 50 scenes and decide to split scene ``02-`` into two separate scenes, you'll need to *re-sequence* the original ``02-`` to be ``03-`` and so on all the way to ``51-``).

Fortunately, just run ``draft sequence`` and Draft will auto-resequence for you.

Compiling
---------

Each directory level corresponds to a Markdown heading level.
When the project compiles, the indices (e.g., ``01-``) are stripped out and each folder's title is inserted as a heading (note: *Scene* titles are ignored).

By running ``draft compile``, the above folder structure would translate into a ``Moby Dick, Or The Whale.md`` file with the following contents:

# Moby Dick, Or The Whale

## Meeting Ishmael

### Nantucket

#### Loomings

Call me Ishmael. Some years ago — never mind how long precisely — having little or no money in my purse, and nothing particular to interest me on shore, I thought I would sail about a little and see the watery part of the world.
It is a way I have of driving off the spleen and regulating the circulation.

Writing
-------

Writing with Draft works best under the following guidelines:

1. **Use Markdown.**

2. **One sentence on each line.**

  This isn't required -- it won't break anything! -- it's just better for tracking changes in Git

3. **Save hash-based Markdown headings for separating sections.**

  If you need to use big font for whatever reason, stick to other header conventions (e.g., ========)

4. **Use Git and Github, and Commit often.**

  Git is incredibly useful in a writing environment and it's branching feature is a godsend if you want to try something radical (e.g., what if we switched from first to third person?).
  Github is a great visualization tool and provides a Cloud storage option for your project.
  And COMMIT-ing often is just good hygiene.

5. **Use a text editor with soft-wrapping and Markdown preview.**

  * **Soft-wrapping:** Keeps your single-line sentences from running off of the page
  * **Markdown preview:** See how your text translates into Markdown
  * `Atom <https://atom.io/>`_ has both of these features
