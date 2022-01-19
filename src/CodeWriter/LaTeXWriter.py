from . import Writer, Block, Listing


def get_parameters_str(required: str, optional: str):
    if optional:
        optional = f"[{optional}]"
    if required:
        required = f"{{{required}}}"
    return optional + required


class Environment(Block):
    def __init__(self, name: str, writer: Writer, required: str = '', optional: str = ''):
        super().__init__(f"\\begin{{{name}}}{get_parameters_str(required, optional)}", f"\\end{{{name}}}", writer)


class LatexListing(Listing):
    def __init__(self, writer, name: str, label: str = "", optional: str = "", item: str = r"\item"):
        if label:
            label = f"label={label}"
        if label or optional:
            optional = f"[{label}" + (f", {optional}]" if optional else "]")
        super().__init__(rf'\begin{{{name}}}' + optional, rf'\end{{{name}}}', writer, item)


class Itemize(LatexListing):
    def __init__(self, writer, label: str = "", optional: str = ""):
        super().__init__(writer, "itemize", label, optional)


class Enumerate(LatexListing):
    def __init__(self, writer, label: str = "", optional: str = ""):
        super().__init__(writer, "enumerate", label, optional)


class LatexWriter(Writer):
    def environment(self, name: str, required: str = '', optional: str = ''):
        return super().block(Environment(name, self, required, optional))

    def itemize(self, label: str = "", optional: str = ""):
        return super().block(Itemize(self, label, optional))

    def enumerate(self, label: str = "", optional: str = ""):
        return super().block(Enumerate(self, label, optional))
