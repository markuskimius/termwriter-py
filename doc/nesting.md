# termwriter-py Documentation

Back to the [Table of Contents]

## 2. Nesting

It is possible to nest boxes to create more elaborate layouts.  Boxes may be
stacked vertically or text may be arranged in a table, for example.

As matter of a fact, `Screen` is a box class itself that flexibly arranges
boxes based on the width of the terminal.  But you shouldn't use Screen
directly to arrange boxes flexibly because `Screen` is a root-level box that:

* Adds a title to every box that is added.
* Prints the boxes to `stdout` at the end of the `with` context.

The box that arranges box flexibly without these additional root-level features
is `FlexBox`.  Other box types are:

* `Table` for arranging boxes in a matrix.
* `Section` for displaying a box with a title.

There is also the `TextBox` class meant for writing text.  It is meant to be
the leaf-level box type complement to the root-level box type `Screen`.

To nest boxes, use the `section()` method to draw a box with a title, or
`draw()` to draw a box without a title.  For example, to vertically stack a
table box under a text box:

```python
from termwriter import Screen
from termwriter import TextBox
from termwriter import Table

with Screen('My Screen') as screen:
    with screen.section('My First Box', Table('l')) as box:
        with box.draw(TextBox()) as tbox:
            tbox.write('I can nest boxes.\n')
            tbox.write('Below is a table:\n')

        with box.draw(Table('ll')) as table:
            table.write('Name:', 'John Q. Public')
            table.write('Tel:', '+1 111 555 3333')
            table.write('Email:', 'nobody@nowhere.com')
```
(The number of characters passed to `Table()` specify the number of columns,
and `l` specifies left-alignment of the table within the cell.)

... which gives the following output:

```
======= My Screen =======

----- My First Box ------
I can nest boxes.
Below is a table:

Name:  John Q. Public
Tel:   +1 111 555 3333
Email: nobody@nowhere.com
```

In contrast, to lay out the text box next to the tabular box horizontally:

```python
from termwriter import Screen
from termwriter import TextBox
from termwriter import Table

with Screen('My Screen') as screen:
    with screen.section('My First Box', Table('ll')) as box:
        with box.draw(TextBox()) as tbox:
            tbox.write('I can nest boxes.\n')
            tbox.write('To the right is a table:\n')

        with box.draw(Table('ll')) as table:
            table.write('Name:', 'John Q. Public')
            table.write('Tel:', '+1 111 555 3333')
            table.write('Email:', 'nobody@nowhere.com')
```
... which gives the following output:

```
=================== My Screen ====================
                                                  
------------------ My First Box ------------------
I can nest boxes.        Name:  John Q. Public    
To the right is a table: Tel:   +1 111 555 3333   
                         Email: nobody@nowhere.com
```

---

Back to the [Table of Contents]


[Table of Contents]: <https://github.com/markuskimius/termwriter-py/blob/master/doc/README.md>

