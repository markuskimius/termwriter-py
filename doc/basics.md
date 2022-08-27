# termwriter-py Documentation

Back to the [Table of Contents]

## 1. The Basics

At the core of `termwriter-py` is the `Screen` class.  Think of `Screen` as a box
within which you can draw more boxes.  It stretches rightward as you add more
boxes, and downward as it wraps boxes to create new rows.

The most common way to instantiate and draw boxes within Screen is using the
`with` context:

```python
from termwriter import Screen
from termwriter import TextBox

with Screen("Screen's Title") as screen:
    with screen.section("My First Box", TextBox()) as box1:
        box1.write("Hello, world!")
        box1.write("This is my first box.")

    with screen.section("My Second Box", TextBox()) as box2:
        box2.write("Hello again!")
        box2.write("This is my second box.")

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


---

Back to the [Table of Contents]


[Table of Contents]: <https://github.com/markuskimius/termwriter-py/blob/master/doc/README.md>

