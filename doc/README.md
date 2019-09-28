# screen-py Documentation

## Overview

`screen-py` is a library to maximize the use of the screen real estate with
`print()`.

The basic concept of `screen-py` is to print text into "boxes" that can be
placed side-by-side to reclaim the unused spaces on the right side of the
terminal.  If too many boxes are placed next to each other, they "wrap" to the
following row, hopefully still within the terminal's viewport, but either way
viewable by scrolling vertically.


## The Basics

At the core of `screen-py` is the `Screen` class.  Think of `Screen` as a box
within which you can draw more boxes.  It stretches rightward as you add more
boxes, and downward as it wraps boxes to create new rows.

The most common way to instantiate and draw boxes within Screen is using the
`with` context:

```python
from screen import Screen

with Screen("Screen's Title") as screen:
    with screen.draw("My First Box") as box1:
        box1.writeln("Hello, world!")
        box1.writeln("This is my first box.")

    with screen.draw("My Second Box") as box2:
        box2.writeln("Hello again!")
        box2.writeln("This is my second box.")
```
... which outputs either:

```
============== Screen's Title ==============
                                            
--- My First Box ---- --- My Second Box ----
Hello, world!         Hello again!          
This is my first box. This is my second box.
```
... or:

```
=== Screen's Title ===
                      
---- My First Box ----
Hello, world!         
This is my first box. 
                      
--- My Second Box ----
Hello again!          
This is my second box.
```
... depending on the viewer's terminal width.


### Why `writeln()`?

The logical choice for the name of the method to print to a box is `print()` in
Python 3.6.  Unfortunately `print` is a reserved keyword in Python 2.7 still
popular as of this writing and cannot be used as the name of a method.  In
order to retain backward compatibility with 2.7, the name of the method of a
similar functionality as `print()` was borrowed from Javascript.

For consistency and utility, boxes also provide the `write()` method.  A
`write(string)` statement followed by a `write('\n')` is equivalent to a single
`writeln(string)` statement.


## Nesting

It is possible to nest boxes to create more elaborate layouts.  Boxes may be
stacked vertically or text may be arranged in a table, for example.

As matter of a fact, `Screen` is a box class itself that flexibly arranges
boxes based on the width of the terminal.  But you shouldn't use Screen
directly to arrange boxes flexibly because `Screen` is a root-level box that:

* Adds a title to every box that is added.
* Prints the boxes to `stdout` at the end of the `with` context.

The box that arranges box flexibly without these additional root-level features
is `FlexBox`.  Other useful boxes are:

* `VerticalBox` for stacking boxes vertically.
* `HorizontalBox` for arranging boxes side-by-side without wrapping.
* `TabularBox` for aligning text like a table-like format.

There is also the `TextBox` class meant for writing text.  It is meant to be
the leaf-level box type complement to the root-level box type `Screen`.

To nest boxes, use the `draw()` method as before, but specify the box type as
the second argument.  For example, to vertically stack a tabular box under a
text box:

```python
from screen import Screen
from screen import TextBox
from screen import TabularBox
from screen import VerticalBox

with Screen('My Screen') as screen:
    with screen.draw('My First Box', VerticalBox) as box:
        with box.draw(TextBox) as tbox:
            tbox.writeln('I can nest boxes.')
            tbox.writeln('Below is a table:')

        with box.draw(TabularBox, 'll') as table:
            table.writeln('Name:', 'John Q. Public')
            table.writeln('Tel:', '+1 111 555 3333')
            table.writeln('Email:', 'nobody@nowhere.com')
```
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
from screen import Screen
from screen import TextBox
from screen import TabularBox
from screen import HorizontalBox

with Screen('My Screen') as screen:
    with screen.draw('My First Box', HorizontalBox) as box:
        with box.draw(TextBox) as tbox:
            tbox.writeln('I can nest boxes.')
            tbox.writeln('To the right is a table:')

        with box.draw(TabularBox, 'll') as table:
            table.writeln('Name:', 'John Q. Public')
            table.writeln('Tel:', '+1 111 555 3333')
            table.writeln('Email:', 'nobody@nowhere.com')
```
... which gives the following output:

```
=================== My Screen ====================
                                                  
------------------ My First Box ------------------
I can nest boxes.        Name:  John Q. Public    
To the right is a table: Tel:   +1 111 555 3333   
                         Email: nobody@nowhere.com
```

A few things about the nested `box.draw()`:

* Unlike a screen, nested boxes do not have title, so the first argument to
  `screen.draw()` is the name of the box class rather than the title for the
  box.

* If no box class is specified as the argument to `draw`, it is assumed to be
  `TextBox`.  So `box.draw(TextBox)` can be simplified to `box.draw()`.

* `draw()` takes a variable number of arguments which is used to instantiate
  the box class.  In the above example, `draw()` passes `'ll'` to `TabularBox`
  to instantiate a tabular box with 2 columns both of which are left-aligned.
  If you wanted, you could have instead instantiated the `TabularBox` with the
  `'ll'` argument first then added it to `box` using `add()`.  For example:
  ```python
        with box.add(TabularBox('ll')) as table:
  ```

