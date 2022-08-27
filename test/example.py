#!/bin/sh

##############################################################################
# BOOTSTRAP
#
# Include ../lib in the search path so we can find termwriter when running locally
# then call python3 or python, whichever exists.
# (See https://unix.stackexchange.com/questions/20880)
#
if "true" : '''\'
then
    export PYTHONPATH="$(dirname $0)/../lib:$PYTHONPATH"
    pythoncmd=python

    if command -v python3 >/dev/null; then
        pythoncmd=python3
    fi

    exec "$pythoncmd" "$0" "$@"
    exit 127
fi
'''

##############################################################################
# PYTHON CODE BEGINS HERE

__copyright__ = "Copyright 2019-2022 Mark Kim"
__license__ = "Apache 2.0"
__version__ = "1.0.0"
__author__ = "Mark Kim"

import sys
import errno
from termwriter import Screen
from termwriter import Section
from termwriter import FlexBox
from termwriter import TextBox
from termwriter import Table
from termwriter import HRule
from termwriter import SoftBreak
from termwriter import HardBreak


def main():
    with Screen('Example Output') as screen:
        screen.write('Some description goes here.')

        with screen.section('My First Box', TextBox()) as box:
            box.write('This is a text box.')

        with screen.section('My Second Box', TextBox()) as box:
            box.write('This is another text box.\n')
            box.write('You can have a second line\n')
            box.write('and it stays in the second box.')

        with screen.section('My Third Box', TextBox()) as box:
            box.write('This box is to the right of the second box.\n')
            box.write('Unless you have a narrow screen --\n')
            box.write('then the box wraps to the next row')

        with screen.section('My Fourth Box', TextBox()) as box:
            box.write('This box stretches to fit the row\n')
            box.write('because we draw SoftBreak()')

        # Soft break causes the current row to full justify and cause the last
        # box to flush right.
        screen.draw(SoftBreak())

        with screen.section('My Fifth Box', TextBox()) as box:
            box.write('Notice the rows are jusified.')

        with screen.section('My Sixth Box', TextBox()) as box:
            box.write('You can also have tables.')

        with screen.section('My First Table', Table('rll')) as table:
            table.write('#', 'First Name', 'Last Name')
            table.draw(HRule())
            table.write(1, 'John', 'Doe')
            table.write(10, 'Jane', 'Doe')
            table.write(100, 'John', 'Public')

        with screen.section('My Eighth Box', TextBox()) as box:
            box.write('You can also nest boxes.\n')
            box.write('Below is a table box.\n')

            with box.draw(Table('ll')) as table:
                table.write('Name:', 'John Q. Public')
                table.write('Tel:', '+1 111 555 3333')
                table.write('Email:', 'nobody@nowhere.com')


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("")
        sys.exit(errno.EOWNERDEAD)


# vim:filetype=python:
