#!/bin/sh

# Include ../lib in the search path so we can find screen.py
# (Thanks to https://unix.stackexchange.com/questions/20880)
if "true" : '''\'
then
    export PYTHONPATH="$(dirname $0)/../lib:$PYTHONPATH"

    exec python "$0" "$@"
    exit 127
fi
'''

import sys
from screen import Screen
from screen import TextBox
from screen import TabularBox


def main():
    with Screen('Example Output') as screen:
        screen.writeln('Some description goes here.')

        with screen.draw('My First Box', TextBox) as box:
            box.writeln('This is a text box.')

        with screen.draw('My Second Box', TextBox) as box:
            box.writeln('This is another text box.')
            box.writeln('You can have a second line')
            box.writeln('and it stays in the second box.')

        with screen.draw('My Third Box', TextBox) as box:
            box.writeln('This box is to the right of the second box.')
            box.writeln('Unless you have a narrow screen --')
            box.writeln('then the box wraps to the next row')

        with screen.draw('My Fourth Box', TextBox) as box:
            box.writeln('This box stretches to fit the row')
            box.writeln('because we call softbreak()')

        # Soft break causes the current row to full justify and cause the last
        # box to flush right.
        screen.softbreak()

        with screen.draw('My Fifth Box', TextBox) as box:
            box.writeln('Notice the rows are jusified.')

        with screen.draw('My Sixth Box', TextBox) as box:
            box.writeln('You can also have tables.')

        with screen.draw('My First Table', TabularBox, 'rll') as table:
            table.writeln('#', 'First Name', 'Last Name')
            table.hrule()
            table.writeln(1, 'John', 'Doe')
            table.writeln(10, 'Jane', 'Doe')
            table.writeln(100, 'John', 'Public')

        with screen.draw('My Eighth Box', TextBox) as box:
            box.writeln('You can also nest boxes.')
            box.writeln('Below is a table box.')
            box.writeln()

            with box.draw(TabularBox, 'll') as table:
                table.writeln('Name:', 'John Q. Public')
                table.writeln('Tel:', '+1 111 555 3333')
                table.writeln('Email:', 'nobody@nowhere.com')


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("")
        sys.exit(errno.EOWNERDEAD)

