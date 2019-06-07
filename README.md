[![codecov](https://codecov.io/gh/edelgm6/draft/branch/master/graph/badge.svg?token=Qh4Eni15kt)](https://codecov.io/gh/edelgm6/draft) [![Build Status](https://travis-ci.com/edelgm6/draft.svg?token=3WrJK2puZHWVDQ14GpNt&branch=master)](https://travis-ci.com/edelgm6/draft)

Draft: Write Like a Programmer
==============================

Draft is a CLI-enabled _writing system_ to keep your work modular, easily use git for version control, and just make writing _fun_ again.

When you're writing something short, a Google Doc or Word file works great. But get beyond a few thousand words and all of a sudden opening that file comes with a sense of dread.

Draft turns that half-finished novel into a clean, plaintext file tree perfect for git.

Primary Features
--------

- `parse` any Markdown file into a file tree of Sections, Chapters, Sub-chapters, and Scenes
- `outline` of your project to help plan and fill in gaps
- `compile` your Scenes, Sub-Chapters, Chapters, and Sections into a single document once you're ready to publish
- Other features include `stats` (e.g., get word count), `trim` (remove duplicate spaces), and `split` (put each sentence on its own line)

Installation
------------

Currently, Draft is only available by cloning this repo and installing locally.
Goal is to be on PyPi with version 0.1.0.

Philosophy of the Draft System
------------------------------

1) Writing in _modules_ (or 'scenes' in Draft lingo) is easier and more fun than working out of a single large document.

2) Writing in plaintext is a more pure and distraction-free experience than [WYSIWYG](https://en.wikipedia.org/wiki/WYSIWYG) word processors.

3) Git is too useful a tool to not use in a writing project.

The System
----------

A Draft project is made up of a simple file tree as shown below:

```
whalebook/
└─project/
│ └──Moby Dick, Or The Whale/ [Title]
│    └──01-Nantucket/ [Sec 1]
│     │ └──01-Meeting Ishmael/ [Chapt 1]
│     │   │   └──01-Loomings/ [Sub-Chapt 1]
│     │   │   │    01-His Name is Ishmael.md [Scene 1]
│     │   │   │    02-Habit of Going To Sea.md [Scene 2]
│     │   │   └──02-The Carpet-Bag/ [Sub-Chapt 2]
│     │   │   │    03-Old Manhatto.md [Scene 3]
│     │   │   │    etc.
│     │   │   └──03-etc.
│     │   └─02-Shoving Off/ [Section 2]
│     │        etc.
│     └──02-Whaling/ [Section 2]
│           etc.
└─.gitignore         
```
You don't _need_ to use every 'level' of the project -- i.e., you could just have the Title and a bunch of scenes, only use sections and scenes, have some scenes in sub-chapters and some scenes in chapters, etc.

The only required elements are the `project/` folder, the `title/` folder, and scene `.md` files.

When the project compiles, the indices (e.g., `01-`) are stripped out and each folder's title is inserted as a heading (note: _Scene_ titles are ignored).
Each level corresponds to a Markdown heading level.  The above folder structure would translate into:

## Moby Dick, Or The Whale

### Nantucket

#### Loomings

Call me Ishmael. Some years ago — never mind how long precisely — having little or no money in my purse, and nothing particular to interest me on shore, I thought I would sail about a little and see the watery part of the world. It is a way I have of driving off the spleen and regulating the circulation.
