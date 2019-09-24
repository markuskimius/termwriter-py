"""A library to maximize the screen real estate.

https://github.com/markuskimius/screen-py
"""

import os, sys

__copyright__ = "Copyright 2019 Mark Kim"
__license__ = "Apache 2.0"


##############################################################################
# UTILITIES

class ScreenUtil(object):
    __cols = None

    @staticmethod
    def termwidth():
        if ScreenUtil.__cols is None:
            # Memoize the terminal width
            try:
                ScreenUtil.__cols = int(os.popen('tput cols', 'r').read())
            except ValueError:
                ScreenUtil.__cols = 120

            # Some terminals line wrap if you try to write to the last column
            # so don't use that column
            ScreenUtil.__cols -= 1

        return ScreenUtil.__cols


class WidgetFormatter(object):
    def __call__(self, lines, width=0, height=0):
        return lines


class LeftFormatter(WidgetFormatter):
    def __init__(self, parent_formatter=WidgetFormatter(), padding_char=' '):
        self.__padding_char = padding_char
        self.__parent_formatter = parent_formatter

    def __call__(self, lines, width=0, height=0):
        lines = self.__parent_formatter(lines, width, height)

        for i, li in enumerate(lines):
            slack = width - len(li)
            padding = self.__padding_char * slack
            lines[i] += padding[0:slack]

        return lines


class RightFormatter(WidgetFormatter):
    def __init__(self, parent_formatter=WidgetFormatter(), padding_char=' '):
        self.__padding_char = padding_char
        self.__parent_formatter = parent_formatter

    def __call__(self, lines, width=0, height=0):
        lines = self.__parent_formatter(lines, width, height)

        for i, li in enumerate(lines):
            slack = width - len(li)
            padding = self.__padding_char * slack
            lines[i] = padding[0:slack] + li

        return lines


class CenterFormatter(WidgetFormatter):
    def __init__(self, parent_formatter=WidgetFormatter(), padding_char=' '):
        self.__padding_char = padding_char
        self.__parent_formatter = parent_formatter

    def __call__(self, lines, width=0, height=0):
        lines = self.__parent_formatter(lines, width, height)

        for i, li in enumerate(lines):
            slack = width - len(li)
            lslack = int(slack / 2)
            rslack = width - (lslack + len(li))
            lpadding = self.__padding_char * lslack
            rpadding = self.__padding_char * rslack
            lines[i] = lpadding[0:lslack] + li + rpadding[0:rslack]

        return lines


class TopFormatter(WidgetFormatter):
    def __init__(self, parent_formatter=WidgetFormatter(), padding_char=' '):
        self.__padding_char = padding_char
        self.__parent_formatter = parent_formatter

    def __call__(self, lines, width=0, height=0):
        lines = self.__parent_formatter(lines, width, height)
        blank = self.__padding_char * width
        blank = blank[0:width]    # Just in case len(padding_char) > 1

        for i in range(len(lines), height):
            lines.append(blank)

        return lines


class BottomFormatter(WidgetFormatter):
    def __init__(self, parent_formatter=WidgetFormatter(), padding_char=' '):
        self.__padding_char = padding_char
        self.__parent_formatter = parent_formatter

    def __call__(self, lines, width=0, height=0):
        tlines = []
        blines = self.__parent_formatter(lines, width, height)
        blank = self.__padding_char * width
        blank = blank[0:width]    # Just in case len(padding_char) > 1

        for i in range(len(blines), height):
            tlines.append(blank)

        return tlines + blines


class MiddleFormatter(WidgetFormatter):
    def __init__(self, parent_formatter=WidgetFormatter(), padding_char=' '):
        self.__padding_char = padding_char
        self.__parent_formatter = parent_formatter

    def __call__(self, lines, width=0, height=0):
        tlines = []
        clines = self.__parent_formatter(lines, width, height)
        blines = []
        blank = self.__padding_char * width
        blank = blank[0:width]    # Just in case len(padding_char) > 1
        vslack = int((height - len(clines)) / 2)

        for i in range(vslack):
            tlines.append(blank)

        for i in range(vslack + len(clines), height):
            blines.append(blank)

        return tlines + clines + blines


class ParagraphFormatter(WidgetFormatter):
    def __init__(self, parent_formatter=WidgetFormatter()):
        self.__parent_formatter = parent_formatter

    def __call__(self, lines, width=0, height=0):
        width = min(width, ScreenUtil.termwidth()) if width else ScreenUtil.termwidth()
        lines = self.__parent_formatter(lines, width, height)
        wrapped = []

        for i, li in enumerate(lines):
            while len(li):
                wrapped.append(li[0:width])
                li = li[width:]

        # Paragraphs have at least an empty text
        if len(wrapped) == 0:
            wrapped.append('')

        return wrapped


NON_FORMATTER = WidgetFormatter()
PARAGRAPH_FORMATTER = ParagraphFormatter()
TOP_LEFT_FORMATTER = TopFormatter(LeftFormatter())
TOP_RIGHT_FORMATTER = TopFormatter(RightFormatter())
TOP_CENTER_FORMATTER = TopFormatter(CenterFormatter())


##############################################################################
# WIDGETS
#
# Widgets go in boxes.

class Widget(object):
    def width(self): return 0
    def height(self): return 0
    def format(self, width=None, height=None): pass


class StringWidget(Widget):
    def __init__(self, string, formatter=PARAGRAPH_FORMATTER):
        self.__string = str(string)
        self.__formatter = formatter

    def width(self):
        lines = self.__string.split('\n')

        return self.__width(lines)

    def height(self):
        lines = self.__string.split('\n')

        return self.__height(lines)

    def __width(self, lines):
        lines = self.__formatter(lines)
        width = 0

        for li in lines:
            width = max(width, len(li))

        return width

    def __height(self, lines):
        lines = self.__formatter(lines)

        return len(lines)

    def format(self, width=None, height=None):
        lines = self.__string.split('\n')

        if width is None: width = self.__width(lines)
        if height is None: height = self.__height(lines)

        return self.__formatter(self.__string.split('\n'), width, height)


class ControlWidget(Widget):
    def format(self, width=None, height=None): return []


class BreakWidget(ControlWidget): pass
class SoftBreak(BreakWidget): pass
class HardBreak(BreakWidget): pass


class FillWidget(ControlWidget):
    def __init__(self, fill_char='*'):
        formatter = LeftFormatter(padding_char=fill_char)
        formatter = TopFormatter(formatter, padding_char=fill_char)

        self.__formatter = formatter

    def format(self, width=None, height=None):
        if width is None: width = self.width()
        if height is None: height = self.height()

        return self.__formatter([], width, height)


class HorizontalRule(FillWidget):
    def __init__(self, rule_char='-'):
        self.__rule_char = rule_char
        super(HorizontalRule, self).__init__(rule_char)

    def height(self):
        return len(self.__rule_char.split('\n'))


class VerticalRule(FillWidget):
    def __init__(self, rule_char='|'):
        self.__rule_char = rule_char
        super(VerticalRule, self).__init__(rule_char)

    def width(self):
        return len(self.__rule_char)


##############################################################################
# BOXES
#
# Boxes contain widgets or other boxes.

class Box(Widget):
    class BoxLockedException(Exception): pass

    def __init__(self):
        self.__widgets = []
        self.__locked = False

    def close(self):
        self.__locked = True

    def add(self, widget):
        if self.__locked: raise BoxLockedException()

        self.__widgets.append(widget)

        return widget

    def remove(self, widget):
        if self.__locked: raise BoxLockedException()

        self.__widgets.remove(widget)

    def __len__(self):
        return len(self.__widgets)

    def __iter__(self):
        for widget in self.__widgets:
            yield widget

    def __getitem__(self, i):
        return self.__widgets[i]

    def __enter__(self):
        return self

    def __exit__(self, type, value, traceback):
        self.close()

    def softbreak(self):
        self.add(SoftBreak())

    def hardbreak(self):
        self.add(HardBreak())

    def hrule(self, rule_char='-'):
        self.add(HorizontalRule(rule_char))

    def vrule(self, rule_char='|'):
        self.add(VerticalRule(rule_char))

    def draw(self, WidgetType=None, *args, **kwargs):
        if WidgetType is None:
            WidgetType = TextBox

        widget = WidgetType(*args, **kwargs)
        self.__widgets.append(widget)

        return widget


class WritableBox(Box):
    def __init__(self):
        super(WritableBox, self).__init__()
        self.__buffer = ''

    def write(self, *args, **kwargs):
        for string in args:
            self.__buffer += str(string)

        lines = self.__buffer.split('\n')

        for li in lines[0:-1]:
            self.add(StringWidget(li))

        self.__buffer = lines[-1]

    def writeln(self, *args, **kwargs):
        for string in args:
            self.write('%s\n' % string, **kwargs)

        if len(args) == 0:
            self.write('\n')

    def close(self):
        if len(self.__buffer): self.write('\n')

        super(WritableBox, self).close()


class HorizontalBox(WritableBox):
    def __init__(self, num_padding=1, formatter=TOP_LEFT_FORMATTER):
        super(HorizontalBox, self).__init__()
        self.__num_padding = num_padding
        self.__formatter = formatter

    def width(self):
        return self.__width()

    def height(self):
        return self.__height()

    def __width(self):
        iterator = super(HorizontalBox, self).__iter__()
        width = 0

        for i, widget in enumerate(iterator):
            width += widget.width()

            # Adjust for spacing between non-control widgets
            if i > 0 and not isinstance(widget, ControlWidget):
                width += self.__num_padding

        return width

    def __height(self):
        iterator = super(HorizontalBox, self).__iter__()
        height = 0

        for i, widget in enumerate(iterator):
            height = max(height, widget.height())

        return max(height, super(HorizontalBox, self).height())

    def format(self, width=None, height=None):
        if height is None: height = self.__height()
        if width is None: width = self.__width()

        justified_widths = self.__justified_widths(width)
        iterator = super(HorizontalBox, self).__iter__()
        padding = ' ' * self.__num_padding
        lines = [''] * height

        for i, widget in enumerate(iterator):
            jw = justified_widths[i]

            if i > 0 and not isinstance(widget, ControlWidget):
                for j in range(height):
                    lines[j] += padding

            for j, li in enumerate(widget.format(jw, height)):
                lines[j] += li

        return self.__formatter(lines, width, height)

    def __justified_widths(self, box_width):
        adj_width = [None] * super(HorizontalBox, self).__len__()
        nat_width = self.__width()
        slack = box_width - nat_width
        pos = 0

        # Don't justify if there is nothing to justify
        if len(adj_width) == 0:
            return adj_width

        # Don't justify if the row ends in a hard break
        last_widget = super(HorizontalBox, self).__getitem__(-1)
        if isinstance(last_widget, HardBreak):
            return adj_width

        # Justify the widgets
        iterator = super(HorizontalBox, self).__iter__()
        for i, widget in enumerate(iterator):
            # No resizing of control widgets
            if isinstance(widget, ControlWidget): continue

            # Update the position for the padding
            if i > 0: pos += self.__num_padding

            # Magic calculation for perfectly resizing the boxes
            width = widget.width()
            remaining = nat_width - pos
            adjustment = int(round(slack * width / remaining)) if remaining else 0
            adj_width[i] = width + adjustment

            # Update the running numbers
            slack -= adjustment
            pos += width

        return adj_width


class VerticalBox(WritableBox):
    def __init__(self, num_padding=1, formatter=TOP_LEFT_FORMATTER):
        self.__num_padding = num_padding
        self.__formatter = formatter

        super(VerticalBox, self).__init__()

    def width(self):
        return self.__width()

    def height(self):
        return self.__height()

    def __width(self):
        iterator = super(VerticalBox, self).__iter__()
        width = 0

        for i, widget in enumerate(iterator):
            width = max(width, widget.width())

        return width

    def __height(self):
        iterator = super(VerticalBox, self).__iter__()
        height = 0

        for i, widget in enumerate(iterator):
            height += widget.height()

            # Adjust for spacing after non-control widgets
            if (i > 0) and not isinstance(widget, ControlWidget):
                height += self.__num_padding

        return height

    def format(self, width=None, height=None):
        iterator = super(VerticalBox, self).__iter__()
        lines = []

        if width is None: width = self.__width()
        if height is None: height = self.__height()
        padding = [' ' * width] * self.__num_padding

        for i, widget in enumerate(iterator):
            for li in widget.format(width):
                lines.append(li)

            # Adjust for spacing after non-control widgets
            if (i > 0) and not isinstance(widget, ControlWidget):
                lines += padding

        return self.__formatter(lines, width, height)


##############################################################################
# DERIVED BOXES

class TabularBox(HorizontalBox):
    class InvalidAlignment(Exception): pass

    def __init__(self, format, num_padding=1, formatter=TOP_CENTER_FORMATTER):
        super(TabularBox, self).__init__(num_padding, formatter)
        self.__columns = []

        for f in format:
            if f == 'l':   textbox = TextBox(TOP_LEFT_FORMATTER)
            elif f == 'r': textbox = TextBox(TOP_RIGHT_FORMATTER)
            elif f == 'c': textbox = TextBox(TOP_CENTER_FORMATTER)
            else: raise TabularBox.InvalidAlignment('%s: Invalid alignment code' % f)

            self.__columns.append(textbox)
            super(TabularBox, self).add(textbox)

    def write(self, *args, **kwargs):
        for i, string in enumerate(args):
            self.__columns[i].write(string, **kwargs)

    def writeln(self, *args, **kwargs):
        for i, string in enumerate(args):
            self.__columns[i].writeln(string, **kwargs)

    def hrule(self, *args, **kwargs):
        for col in self.__columns:
            col.hrule(*args, **kwargs)

    def close(self):
        for col in self.__columns:
            col.close()


class TextBox(VerticalBox):
    def __init__(self, formatter=TOP_LEFT_FORMATTER):
        super(TextBox, self).__init__(num_padding=0, formatter=formatter)


class FlexBox(WritableBox):
    def __init__(self, max_width=ScreenUtil.termwidth(), formatter=TOP_LEFT_FORMATTER, num_hpadding=1, num_vpadding=1):
        self.__num_hpadding = num_hpadding
        self.__num_vpadding = num_vpadding
        self.__max_width = max_width
        self.__formatter = formatter
        self.__vbox = Box()

        super(FlexBox, self).__init__()

    def width(self):
        return self.__vbox.width()

    def height(self):
        return self.__vbox.height()

    def close(self):
        iterator = super(FlexBox, self).__iter__()
        maxwidth = self.__max_width
        vbox = VerticalBox(self.__num_vpadding, self.__formatter)
        hbox = HorizontalBox(self.__num_hpadding, self.__formatter)

        # Arrange our widgets so widgets do not go past the terminal width
        for i, widget in enumerate(iterator):
            hbox.add(widget)

            # If we added too much, break
            if hbox.width() > maxwidth:
                hbox.remove(widget)         # Remove the last widget

                vbox.add(hbox)
                hbox = HorizontalBox(self.__num_hpadding, self.__formatter)

                hbox.add(widget)            # Add it back to the new hbox

            # If requested, break
            elif isinstance(widget, BreakWidget):
                vbox.add(hbox)
                hbox = HorizontalBox(self.__num_hpadding, self.__formatter)

        # Last hbox
        if len(hbox):
            hbox.hardbreak()
            vbox.add(hbox)

        # Commit
        self.__vbox = vbox
        # super(FlexBox, self).close()

    def format(self, width=None, height=None):
        return self.__vbox.format(width, height)


##############################################################################
# BOX DECORATORS

class TitledBox(VerticalBox):
    def __init__(self, title, box, hrule='-'):
        decorated_title = '%s %s %s' % (hrule, title, hrule)
        self.__title = StringWidget(decorated_title, CenterFormatter(padding_char=hrule))
        self.__content = box

        super(TitledBox, self).__init__(num_padding=0)
        super(TitledBox, self).add(self.__title)
        super(TitledBox, self).add(self.__content)

    def close(self):
        self.__content.close()

    def add(self, widget):
        self.__content.add(widget)

        return widget

    def remove(self, widget):
        self.__content.remove(widget)

    def __len__(self):
        return len(self.__content)

    def __iter__(self):
        for widget in self.__content.__iter__():
            yield widget

    def __getitem__(self, i):
        return self.__content[i]

    def write(self, *args, **kwargs):
        self.__content.write(*args, **kwargs)

    def writeln(self, *args, **kwargs):
        self.__content.writeln(*args, **kwargs)

    def softbreak(self):
        self.__content.softbreak()

    def hardbreak(self):
        self.__content.hardbreak()

    def hrule(self, *args, **kwargs):
        self.__content.hrule(*args, **kwargs)

    def vrule(self, *args, **kwargs):
        self.__content.vrule(*args, **kwargs)

    def draw(self, WidgetType=TextBox, *args, **kwargs):
        return self.__content.draw(WidgetType, *args, **kwargs)


##############################################################################
# SCREEN

class Screen(TitledBox):
    def __init__(self, title, fp=sys.stdout, hrule='='):
        self.__console = TextBox()   # Create a console area
        self.__fp = fp               # We'll use this at __exit__

        super(Screen, self).__init__(title, FlexBox(), hrule=hrule)  # I am a FlexBox with a title!
        super(Screen, self).add(self.__console)                      # Add the console to the screen
        super(Screen, self).hardbreak()                              # Other boxes go below the console

    def write(self, *args, **kwargs):
        # Writing to the screen writes to the console area.
        self.__console.write(*args, **kwargs)

    def writeln(self, *args, **kwargs):
        # Writing to the screen writes to the console area.
        self.__console.writeln(*args, **kwargs)

    def add(self, title, box):
        # All boxes added to the Screen get a title
        box = TitledBox(title, box)      # Add a title
        super(Screen, self).add(box)     # Add the box to myself

        return box

    def draw(self, title, BoxType=TextBox, *args, **kwargs):
        # All boxes added to the Screen get a title
        box = BoxType(*args, **kwargs)   # Create the box
        box = TitledBox(title, box)      # Add a title
        super(Screen, self).add(box)     # Add the box to myself

        return box

    def close(self):
        super(Screen, self).close()

        # Write it out to fp (sys.stdout by default)
        for line in super(Screen, self).format():
            self.__fp.write(str(line))
            self.__fp.write('\n')

