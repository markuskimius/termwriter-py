# screen-py Documentation

[<-] Back to the [Table of Contents]

## 1. The Basics

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


---

[<-] Back to the [Table of Contents]


               [<-]: <https://github.com/markuskimius/screen-py/blob/master/doc/README.md>
[Table of Contents]: <https://github.com/markuskimius/screen-py/blob/master/doc/README.md>

