# screen-py

A library to maximize the screen real estate utility with print().


## Motivation

Dumping a ton of information to the screen using `print()` can cause the data
you want to see on the screen to scroll up and away.  This can be particularly
frustrating because today's monitors have a lot more horizontal screen space
but the data scrolls away vertically.  What if the data can be better output to
maximize the screen real estate?


## Example Output

```
================================ Example Output ================================
Some description goes here.

------- My First Box -------- ----------------- My Second Box ------------------
This is a text box.           This is another text box.
                              You can have a second line
                              and it stays in the second box.

--------------- My Third Box --------------- ---------- My Fourth Box ----------
This box is to the right of the second box.  This box stretches to fit the row
Unless you have a narrow screen --           because we call softbreak()
then the box wraps to the next row

------- My Fifth Box -------- ----- My Sixth Box ------ ---- My First Table ----
Notice the rows are jusified. You can also have tables.   # First Name Last Name
                                                        --- ---------- ---------
                                                          1 John       Doe
                                                         10 Jane       Doe
                                                        100 John       Public

----- My Eighth Box -----
You can also nest boxes.
Below is a table box.

Name:  John Q. Public
Tel:   +1 111 555 3333
Email: nobody@nowhere.com
```


## Usage

TBD


## Example

See [example.py]


## License

[Apache 2.0]


[example.py]: <https://github.com/markuskimius/screen-py/blob/master/test/example.py>
[Apache 2.0]: <https://github.com/markuskimius/screen-py/blob/master/LICENSE>

