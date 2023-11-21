from __future__ import annotations
import sys
import warnings
from typing import Union


class Writer:
    """
    Base class for code writing.

    Use the method 'print' for writing correctly intended code. The 'block' should be used in a with statement and
    increases the indentation level for all print statements in the with statement, except for the entry and exit line.
    The 'listing' method provides a way to create indented listings and should also be used in a with statement. Use the
    item method for new items inside a listing.

    """

    def __init__(self, indentation: str = ' ' * 4, indentation_level: int = 0, file=sys.stdout):
        """
        Creates a new Writer object.
        :param indentation: str, optional
            String, which is used for indenting.
        :param indentation_level:  int, optional
            Starting indentation_level
        :param file: object, optional
            See `file` argument of standard print method: https://docs.python.org/3/library/functions.html#print
        """
        self.indentation = indentation
        self.indentation_level = indentation_level
        self.file = file
        # list of all currently active blocks
        self.blocks: list[Block] = []

    def __get_indentation(self) -> str:
        """
        Gets the current indentation.

        :return: str
            current indentation
        """
        return self.indentation * self.indentation_level

    def extend_newline(self, s: str) -> str:
        return s.replace('\n', f'\n{self.__get_indentation()}')

    def print(self, *args, sep=' ', end='\n', flush=False):
        """
        Works like the normal `print` function (see: https://docs.python.org/3/library/functions.html#print), except it
        indents the first argument of args and the file parameter is given by the object itself as specified in
        `__init__`.
        :param args:
            arguments which should be printed. Note: the newline character '\n' gets extended with the current
            indentation.
        :param sep: str, optional
            The printed separator between arguments. Note: the newline character '\n' gets extended with the
            current indentation.
        :param end: str, optional
            String which gets printed after the last argument. Note: If the last character is not a newline
            character, correct indentation can not be guaranteed!
        :param flush: bool, optional
            See: https://docs.python.org/3/library/functions.html#print
        """
        # check for linebreaks in the arguments
        args = [self.extend_newline(str(arg)) for arg in args]
        # check for linebreaks in the separator
        # extend linebreak with current indentation to guarantee correct indentation and warn user
        sep = self.extend_newline(sep)
        # if the last character of 'end' is not a newline character warn the user
        if '\n' != end[-1]:
            warnings.warn("There is no linebreak in 'end' or it is not at the end of 'end'."
                          "Correct indentation can not be guaranteed!", UserWarning)
        # Start by indenting
        print(self.__get_indentation(), end='', file=self.file)
        # print arguments
        print(*args, sep=sep, end=end, flush=flush, file=self.file)

    def block(self, entry_line: Union[str, Block], exit_line: str = '') -> Block:
        """
        Creates a new indentation block.
        :param entry_line: str or Block
            String, which gets printed upon entering the block or an already initialized block.
        :param exit_line: str, optional
            String, which gets printed upon exiting the block.
        :return: Block
            Returns the block for use in `with` statement.
        """
        # Check if a new block has to be created or not.
        if isinstance(entry_line, str):
            block = Block(entry_line, exit_line, self)
        elif isinstance(entry_line, Block):
            block = entry_line
        else:
            raise TypeError("The argument 'entry_line' has to be either an instance of a 'str' or of a 'Block'.")
        # Append block to block list
        self.blocks.append(block)
        return block

    def listing(self, entry_line: str, item: str, exit_line: str = '') -> Block:
        """
        Creates a new indented listing.
        :param entry_line: str
            String, which gets printed upon entering the block.
        :param item: str
            String, which gets printed, when calling the `item` method.
        :param exit_line: str, optional
            String, which gets printed upon exiting the block.
        :return: Block
            Returns the block for us in `with` statement.
        """
        return self.block(Listing(entry_line, exit_line, self, item))

    def item(self, line: str = ''):
        """
        Function for printing a new item in a listing.
        :param line: str, optional
            String, which gets printed after the item string separated by a whitespace.
        """
        # First check if there is a block at all and if it is a Listing.
        try:
            block = self.blocks[-1]
            assert isinstance(block, Listing)
        except AssertionError:
            raise RuntimeError(f"You are currently in a '{type(block)}' not in a 'Listing'!")
        except IndexError:
            raise RuntimeError("There are currently no Listings!")
        # If there was already an item before, decrease the indentation_level
        if block.in_item:
            self.indentation_level -= 1
        # print the item with the given line
        self.print(block.item, line)
        # set `in_item` to True, because now there was definitely at least one item
        block.in_item = True
        # increase indentation for upcoming text under the same item
        self.indentation_level += 1


class Block:
    """
    Parent class for creating indentation Blocks.
    A `Block` object is supposed to be used in a `with` statement, which starts the indentation and automatically ends
    it upon exiting.
    It should be created by the block method inside the `Writer` class or at least passed as the argument of the method.
    """

    def __init__(self, entry_line: str, exit_line: str, writer: Writer):
        """
        Create a new `Block` object.
        :param entry_line: str
            String, which gets printed upon entering the block.
        :param exit_line: str
            String, which gets printed upon exiting the block.
        :param writer: Writer
            `Writer` object, which keeps track of indentation and the printing.
        """
        self.exit_line = exit_line
        self.entry_line = entry_line
        self.writer = writer

    def __enter__(self):
        # upon entering a block print the entry line and extend possible newline characters
        self.writer.print(self.writer.extend_newline(self.entry_line))
        # increase indentation level
        self.writer.indentation_level += 1

    def __exit__(self, exc_type, exc_val, exc_tb):
        # upon exiting a block decrease indentation level
        self.writer.indentation_level -= 1
        # print the exit line and extend possible newline characters
        if self.exit_line:
            self.writer.print(self.writer.extend_newline(self.exit_line))
        # remove this `Block` from the block list of the writer
        self.writer.blocks.pop()


class Listing(Block):
    """
    Subclass of `Block` for creating itemized listings.
    """
    def __init__(self, entry_line: str, exit_line: str, writer: Writer, item: str):
        """
        Create a new `Listing` object.
        :param entry_line: str
            String, which gets printed upon entering the block.
        :param exit_line: str
            String, which gets printed upon exiting the block.
        :param writer: Writer
            `Writer` object, which keeps track of indentation and the printing.
        :param item: str
            The symbol for a new list entry.
        """
        super().__init__(entry_line, exit_line, writer)
        self.item = item
        # boolean value for storing whether an item was already printed
        self.in_item = False

    def __exit__(self, exc_type, exc_val, exc_tb):
        # decrease indentation one more time, if an item was printed
        if self.in_item:
            self.writer.indentation_level -= 1
        super().__exit__(exc_type, exc_val, exc_tb)
