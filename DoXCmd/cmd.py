# some other useful imports
import datetime, re, shlex, sys
# add DoX core to path
sys.path.append("dox")
# main class import
from dox import *

class main:
    dox = None
    needSave = False
    def __init__(self):
        # create DoX API object
        self.dox = dox()
        args = sys.argv[1:]
        # no arguments, default to list
        if not len(args):
            args = ["list"]
        self.cmd(args, False)
        if self.needSave:
            self.dox.saveTasks()
    def cmd(self, args, shell):
        args[0] = args[0].lower()
        print("")
        # trying to use "dox" in a shell
        if args[0] == "dox" and shell:
            print("You don't need to prefix commands with \"dox\" here.")
        # show a list of all tasks
        elif args[0] in ["list", "l"]:
            self.list(args)
        # add a new task to the list
        elif args[0] in ["add", "a"]:
            self.add(args)
        # edit an existing task
        elif args[0] in ["edit", "e"]:
            self.edit(args)
        # show info about the task
        elif args[0] in ["info", "i"]:
            self.info(args)
        # move a task in the list
        elif args[0] in ["move", "m"]:
            self.move(args)
        # mark a task as complete
        elif args[0] in ["done", "d"]:
            self.done(args)
        # unmark a task as complete
        elif args[0] in ["undo", "d"]:
            self.undo(args)
        # remove a task without completing
        elif args[0] in ["del", "x"]:
            self.delete(args)
        # interactive DoX shell
        elif args[0] == "shell":
            # no recursion allowed :P
            if shell:
                print("You can't launch a shell from a shell...")
            else:
                # welcome message
                print("DoX interactive shell: type \"help\" for a list of commands.\n")
                # enter shell loop
                while True:
                    try:
                        # get a command
                        args = shlex.split(raw_input("DoX > "))
                    # parse error (e.g. no closing quote)
                    except ValueError:
                        print("\nInvalid command; type \"help\" for a list of commands.\n")
                        args = []
                    # user interrupted or ended session, end shell
                    except (KeyboardInterrupt, EOFError):
                        print("exit\n")
                        sys.exit(0)
                    if len(args):
                        # quit command, end shell
                        if args[0] in ["exit", "quit", "q"]:
                            print("")
                            sys.exit(0)
                        else:
                            # run command in shell mode
                            self.cmd(args, True)
        # reload the tasks file now (shell only)
        elif args[0] in ["load", "o"]:
            if shell:
                self.load(args)
            # not in a shell, nothing to do
            else:
                print("Not running in a shell, so nothing to do here.")
        # save the tasks file now (shell only)
        elif args[0] in ["save", "s"]:
            if shell:
                self.save(args)
            # not in a shell, nothing to do
            else:
                print("Not running in a shell, so nothing to do here.")
        # display command help
        elif args[0] in ["help", "h", "?"]:
            # help text; prefix commands with "dox" when not in shell
            print("""================================
DoX: terminal to-do list manager
================================

Commands
--------
{0}list [raw] [done] [+/-<field>] [#<tag>]
{0}add [<title>] [~<desc>] [0|![![!]]|!<pri>] [#<tag>]
{0}edit <id> [<title>] [~<desc>] [0|![![!]]|!<pri>] [#<tag>]
{0}info <id>
{0}move <id> [<pos>]
{0}done|undo <id>
{0}del <id>
{1}

Listing your tasks
------------------
* Use `{0}list` to show all tasks in your list.
* Append `+<field>` for ascending sort, or `-<field>` for descending.
* Filter by tag adding `#<tag>`.
* Mutliple sorts and filters can be used.
* Use raw to show your tasks as DoX strings (as they would appear in tasks.txt).
* View more information on a task with `info <id>`.

Adding tasks
------------
* Use `{0}add <title>` to add a quick task.
* Add a description by appending `~<desc>`.
* Wrap multiple word values in quotes.
* Set the priority to `0`, or use up to three `!` marks for 1 to 3.
* Assign tags using `#<tag>`.  Multiple tags are written `#<tag1> #<tag2>...`.

Completing tasks
----------------
* Use `{0}done <id>` to mark a task as complete and remove it from the list.
* Use `{0}del <id>` to remove without completing.""".format(("" if shell else "dox "), ("load|save\nhelp\nexit" if shell else "dox shell\ndox help")))
        # unrecognized command
        else:
            print("Unknown command \"{}\"; type \"{}help\" for a list of commands.".format(args[0], ("" if shell else "dox ")))
        print("")
    def list(self, args):
        tasks = self.dox.tasks
        # to handle after all arguments searched
        toSort = []
        toSub = []
        done = False
        raw = False
        # additional arguments
        if len(args) > 1:
            # loop arguments
            for i in range(1, len(args)):
                arg = args[i]
                # sort the list
                if re.match("^[\+-]", arg):
                    desc = arg[0] == "-"
                    field = arg[1:]
                    # user-friendly aliases
                    if field in ["task", "name"]:
                        field = "title"
                    elif field in ["description", "details", "info", "~"]:
                        field = "desc"
                    elif field in ["priority", "!"]:
                        field = "pri"
                    elif field in ["date", "time", "@"]:
                        field = "due"
                    elif field in ["tag", "#"]:
                        field = "tags"
                    toSort.append((field, desc))
                # filter by a tag
                elif arg[0] == "#":
                    toSub.append(("tag", arg[1:]))
                # filter by due date
                elif arg[0] == "@":
                    tag = arg[1:]
                    toSub.append(("due", arg[1:]))
                # display from done list instead of to-do
                elif arg == "done":
                    done = True
                # display DoX string format lines (ie. as they would appear in tasks.txt)
                elif arg == "raw":
                    raw = True
        # if showing completed tasks, swap list to show
        if done:
            tasks = self.dox.done
        # reverse sort arguments (so first sort field is applied last but appears first)
        toSort.reverse()
        # apply sort in order
        for sort in toSort:
            # sort with undefined items at bottom regardless of order
            withField = sorted([x for x in tasks if not getattr(x, sort[0]) is None], key=(lambda x: getattr(x, sort[0])), reverse=sort[1])
            withoutField = [x for x in tasks if getattr(x, sort[0]) is None]
            tasks = withField + withoutField
        # now filter by tags
        for sub in toSub:
            if sub[0] == "tag":
                tag = sub[1]
                filtered = []
                # remove any tasks not matching the given tag
                for taskObj in tasks:
                    if tag.lower() in [x.lower() for x in taskObj.tags]:
                        filtered.append(taskObj)
                # replace task list
                tasks = filtered
            elif sub[0] == "due":
                keyword = sub[1]
                filtered = []
                for taskObj in tasks:
                    if taskObj.due:
                        today = datetime.datetime.today().date()
                        due = taskObj.due.date()
                        # show all tasks with a due date
                        cond = (keyword in ["due", "date", "time"])
                        # or only show tasks due today
                        cond |= (keyword in ["today", "now"] and due == today)
                        # or only show tasks due tomorrow
                        cond |= (keyword in ["tomorrow"] and due == today + datetime.timedelta(days=1))
                        # or only show tasks due in the next 7 days
                        cond |= (keyword in ["soon", "week", "this week"] and today <= due <= today + datetime.timedelta(days=7))
                        # or only show overdue tasks
                        cond |= (keyword in ["overdue", "late"] and due < today)
                        # task matches the criteria
                        if (cond):
                            filtered.append(taskObj)
                # replace task list
                tasks = filtered
        # if there are tasks
        if len(tasks):
            if raw:
                for taskObj in tasks:
                    print(taskObj)
            else:
                # table layout - four columns
                tmpl = "{:1}  {:32}  {:1}  {:19}  {:32}"
                # table header
                print("-" * 93)
                print(tmpl.format("#", "Task", "!", "Due", "Tags"))
                print("-" * 93)
                for taskObj in tasks:
                    # table row
                    print(tmpl.format(taskObj.id, (util.trunc(taskObj.title, 32) if taskObj.title else "<unnamed task>"), taskObj.pri,
                                      (taskObj.due.strftime("%d/%m/%Y %H:%M:%S") if taskObj.due else "<none>"),
                                      util.trunc(", ".join(taskObj.tags), 32) if taskObj.tags else "<none>"))
                print("-" * 93)
        # no tasks in file
        else:
            print("No tasks in your list that match the current filters.")
    def add(self, args):
        title, desc, pri, due, tags = util.parseArgs(args[1:])
        if title or desc or pri or len(tags):
            # add task via DoX interface
            self.dox.addTask(title, desc, pri, due, tags)
            print("Added task \"{}\".".format(title))
        # no valid arguments given
        else:
            print("Usage: add [<title>] [~<desc>] [0|![![!]]] [#<tag>]")
    def edit(self, args):
        # if id is valid
        if len(args) > 2 and args[1].isdigit() and not args[1] == "0":
            id = int(args[1])
            if id > 0 and id <= len(self.dox.tasks):
                # fetch the task
                taskObj = self.dox.getTask(id)
                title, desc, pri, due, tags = util.parseArgs(args[2:], taskObj.title, taskObj.desc, taskObj.pri, taskObj.due, taskObj.tags)
                # edit task via DoX interface
                self.dox.editTask(id, title, desc, pri, due, tags)
                print("Updated task \"{}\".".format(title))
            # invalid id
            else:
                print("No task found for ID \"{}\".".format(id))
        # no valid arguments given
        else:
            print("Usage: edit <id> [<title>] [~<desc>] [0|![![!]]] [#<tag>]")
    def info(self, args):
        # if id is valid
        if len(args) > 1     and args[1].isdigit() and not args[1] == "0":
            id = int(args[1])
            if id > 0 and id <= len(self.dox.tasks):
                # fetch the task
                taskObj = self.dox.getTask(id)
                out = []
                if taskObj.title:
                    out.append("{}\n{}".format(taskObj.title, ("-" * len(taskObj.title))))
                    out.append("")
                if taskObj.desc:
                    out.append(taskObj.desc)
                    out.append("")
                if taskObj.due:
                    out.append("Due: {}".format(taskObj.due.strftime("%d/%m/%Y %H:%M:%S")))
                out.append("Priority: {}".format(taskObj.pri))
                if taskObj.tags:
                    out.append("")
                    out.append("#{}".format(" #".join(taskObj.tags)))
                print("\n".join(out))
            # invalid id
            else:
                print("No task found for ID \"{}\".".format(id))
        # no valid arguments given
        else:
            print("Usage: info <id>")
    def move(self, args):
        # if id is valid
        if len(args) >= 2 and args[1].isdigit() and not args[1] == "0":
            id = int(args[1])
            # default to move to end of list
            pos = len(self.dox.tasks)
            if len(args) >= 3:
                # if pos is valid
                if args[2] in ["0", "start", "front", "top", "first"]:
                    pos = 1
                elif args[2].isdigit():
                    pos = int(args[2])
                    if pos > len(self.dox.tasks):
                        pos = len(self.dox.tasks)
            # if valid move
            if id > 0 and id <= len(self.dox.tasks):
                # id and pos different
                if not id == pos:
                    self.dox.moveTask(id, pos)
                    print("Moved task from position {} to {}.".format(id, pos))
                else:
                    print("The task is already in that position.")
            # invalid id
            else:
                print("No task found for ID \"{}\".".format(id))
        # no valid arguments given
        else:
            print("Usage: move <id> [<pos>]")
    def done(self, args):
        # if id is valid
        if len(args) > 1 and args[1].isdigit() and not args[1] == "0":
            id = int(args[1])
            if id > 0 and id <= len(self.dox.tasks):
                taskObj = self.dox.getTask(id)
                self.dox.doneTask(id)
                print("Completed task \"{}\".  Well done!".format(taskObj.title))
            # invalid id
            else:
                print("No task found for ID \"{}\".".format(id))
        # no valid arguments given
        else:
            print("Usage: done <id>")
    def undo(self, args):
        # if id is valid
        if len(args) > 1 and args[1].isdigit() and not args[1] == "0":
            id = int(args[1])
            if id > 0 and id <= len(self.dox.done):
                taskObj = self.dox.getDone(id)
                self.dox.undoTask(id)
                print("Reverted state of task \"{}\"...".format(taskObj.title))
            # invalid id
            else:
                print("No task found for ID \"{}\".".format(id))
        # no valid arguments given
        else:
            print("Usage: undo <id>")
    def delete(self, args):
        # if id is valid
        if len(args) > 1 and args[1].isdigit() and not args[1] == "0":
            id = int(args[1])
            if id > 0 and id <= len(self.dox.tasks):
                taskObj = self.dox.getTask(id)
                if raw_input("Deleting the task \"{}\", are you sure (yes/no)? ".format(taskObj.title)) in ["yes", "y"]:
                    self.dox.deleteTask(id)
                    print("Deleted task \"{}\".".format(taskObj.title))
                else:
                    print("Aborted, kept the task.")
            # invalid id
            else:
                print("No task found for ID \"{}\".".format(id))
        # no valid arguments given
        else:
            print("Usage: del <id>")
    def save(self, args):
        # save tasks via DoX interface
        self.dox.saveTasks()
        print("Your tasks have been saved.")
    def load(self, args):
        # load tasks via DoX interface
        self.dox.loadTasks()
        print("Your tasks have been loaded.")

if __name__ == "__main__":
    # Python 2/3 compatibility hack: allows use of raw_input in Python 3.x
    if not "raw_input" in dir(__builtins__):
        def raw_input(prompt):
            return input(prompt)
    # start!
    main()
