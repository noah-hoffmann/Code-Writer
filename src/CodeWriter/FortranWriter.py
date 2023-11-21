from . import Writer, Block
import textwrap


class Function(Block):
    def __init__(self, writer: Writer, name: str, *args: str, result: str = None,
                 elemental=False, pure=False, trailing=True):
        if result is not None:
            result = f" result({result})"
        else:
            result = ""

        if elemental:
            method = "elemental function"
        elif pure:
            method = "pure function"
        else:
            method = "function"
        super().__init__(
            f"{method} {name}({', '.join(args)}){result}",
            f"end function {name}" + ('\n' if trailing else ''),
            writer
        )


class Subroutine(Block):
    def __init__(self, writer: Writer, name: str, *args: str, trailing=True):
        super().__init__(
            f"subroutine {name}({', '.join(args)})",
            f"end subroutine {name}" + ('\n' if trailing else ''),
            writer
        )


class Module(Block):
    def __init__(self, writer: Writer, name: str):
        super().__init__(f"module {name}",
                         f"end module {name}",
                         writer)


class FortranWriter(Writer):
    def function(self, name: str, *args: str, result: str = None, elemental=False, pure=False,
                 trailing=True):
        return super().block(Function(self, name, *args, result=result, elemental=elemental, pure=pure,
                                      trailing=trailing))

    def subroutine(self, name: str, *args: str, trailing=True):
        return super().block(Subroutine(self, name, *args, trailing=trailing))

    def module(self, name: str):
        return super().block(Module(self, name))

    def comment(self, comment: str, flush=False, dedent=True):
        if dedent:
            comment = textwrap.dedent(comment)
        comment = f"! {comment}"
        comment = comment.replace('\n', "\n! ")
        self.print(comment, flush=flush)

    def use(self, module: str, flush=False):
        self.print(f"use {module}", flush=flush)

    def declare(self, type: str, *variables: str, allocatable=False, intent=None, flush=False):
        declaration = type
        if allocatable:
            declaration = f"{declaration}, allocatable"
        if intent is not None:
            declaration = f"{declaration}, intent({intent})"
        self.print(f"{declaration} :: {', '.join(variables)}")

    def contains(self, flush=False):
        self.indentation_level -= 1
        self.print("contains", flush=flush)
        self.indentation_level += 1
