from . import Writer, Block, Listing


class Function(Block):
    def __init__(self, writer: Writer, name: str, *args: str, return_type: str = ""):
        if return_type:
            return_type = f" -> {return_type}"
        super().__init__(f"def {name}({', '.join(args)}){return_type}:", " ", writer)


class Class(Block):
    def __init__(self, writer: Writer, name: str, *args: str):
        arguments = ', '.join(args)
        if arguments:
            arguments = f"({arguments})"
        super().__init__(f"class {name}{arguments}:", " ", writer)


class ForLoop(Block):
    def __init__(self, writer: Writer, variable: str, iterable: str):
        super().__init__(f"for {variable} in {iterable}:", "", writer)


class RangeLoop(ForLoop):
    def __init__(self, writer: Writer, variable: str, start: int, stop: str = "", step: str = ""):
        arguments = ", ".join((s for s in (start, stop, step) if s))
        super().__init__(writer, variable, f"range({arguments})")


class WhileLoop(Block):
    def __init__(self, writer: Writer, condition: str):
        super().__init__(f"while {condition}:", "", writer)


class IfStatement(Listing):
    def __init__(self, writer: Writer, condition: str):
        super().__init__(f"if {condition}:", "", writer, "else:")


class PythonWriter(Writer):
    def function(self, name: str, *args: str, return_type: str = ""):
        return super().block(Function(self, name, *args, return_type=return_type))

    def new_class(self, name: str, *args):
        return super().block(Class(self, name, *args))

    def for_loop(self, variable: str, iterable: str):
        return super().block(ForLoop(self, variable, iterable))

    def range_loop(self, variable: str, start: str, stop: str = "", step: str = ""):
        return super().block(RangeLoop(self, variable, start, stop, step))

    def while_loop(self, condition: str):
        return super().block(WhileLoop(self, condition))

    def if_statement(self, condition: str):
        return super().block(IfStatement(self, condition))

    def else_statement(self):
        try:
            block = self.blocks[-1]
            assert isinstance(block, IfStatement)
        except AssertionError:
            raise RuntimeError(f"You are currently in a '{type(block)}' not in a 'IfStatement'!")
        except IndexError:
            raise RuntimeError("There are currently no Listings!")
        self.indentation_level -= 1
        self.print("else:")
        self.indentation_level += 1

    def elif_statement(self, condition: str):
        try:
            block = self.blocks[-1]
            assert isinstance(block, IfStatement)
        except AssertionError:
            raise RuntimeError(f"You are currently in a '{type(block)}' not in a 'IfStatement'!")
        except IndexError:
            raise RuntimeError("There are currently no Listings!")
        self.indentation_level -= 1
        self.print("elif", f"{condition}:")
        self.indentation_level += 1
