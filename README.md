Introduction
------------

DoX is a feature-packed to-do list application in Python.  DoXCmd allows you to add, manage and complete your tasks from the command line.

Tasks to do are stored in tasks.txt, and completed tasks in done.txt, both in the DoX folder in your home directory.

The shell command provides an interpreter to read a series of DoX commands without the prefix each time.  Note `load` and `save` are only available in shell mode.


Prerequisites
-------------

This program relies on the DoX API, which is not included in this package.  You must [download](http://github.com/OllieTerrance/DoX) and install it separately, then provide a copy of the files (through symlink or otherwise) in a `dox` folder within the `DoXCmd` folder.


Commands
--------

Note that these commands start with `dox`, assuming these will call `cmd.py`.  You may wish to set up an alias or script to do this for you.

    dox list [raw] [done] [+/-<field>] [#<tag>]
    dox add [<title>] [~<desc>] [0|![![!]]|!<pri>] [@<due>] [&<repeat>[*]] [#<tag>]
    dox edit <id> [<title>] [~<desc>] [0|![![!]]|!<pri>] [@<due>] [&<repeat>[*]] [#<tag>]
    dox info <id>
    dox move <id> [<pos>]
    dox done|undo <id>
    dox del <id>
    dox load|save
    dox shell
    dox help
    dox exit


Listing your tasks
------------------

* Use `dox list` to show all tasks in your list.
* Append `+<field to sort by>` for ascending sort, or `-<field>` for descending.
* Filter by tag adding `#<tag>`.
* Mutliple sorts and filters can be used (sorts are applied in order).
* Use raw to show your tasks as DoX strings (as they would appear in tasks.txt).
* View more information on a task with `dox info <id>`.
* Move tasks around in the list using `dox move <id> <new position>`.


Adding tasks
------------

* Use `dox add <title>` to add a quick task.
* Add a description by appending `~<description>`.
* Wrap multiple words in quotes.
* The priority can be set with `!<level>`, for a level between `0` and `3`.  You can
  also set the priority to `0`, or use up to three `!` marks for 1 to 3.
* Set a due date with `@<when>`.  Absolute and relative (eg. "tomorrow") dates/times
  are supported.  Split the date from the time using a `|`.
* Make the task repeat with `&<when>`.  Enter a number of days or a relative time (eg.
  "daily").  Repeats occur from the due date; append `*` to repeat from today instead.
* Assign tags using `#<tag>`.  Multiple tags are written `#<tag1> #<tag2>...`.


Completing tasks
----------------

* Use `dox done <id>` to mark a task as complete and remove it from the list.
* Undo a task with `dox undo <id>` (you can find the new ID with `dox list done`).
* Use `dox del <id>` to remove without completing.
