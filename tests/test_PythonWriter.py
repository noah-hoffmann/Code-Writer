from io import StringIO

from CodeWriter import PythonWriter


def test_PythonWriter():
    buffer = StringIO()
    writer = PythonWriter(file=buffer)

    with writer.new_class("ClassA", "int", "str"):
        with writer.function("__init__", "self", return_type="None"):
            writer.print("pass")

    with writer.new_class("ClassB"):
        writer.print("pass")

    with writer.function("main"):
        with writer.if_statement("condition 1"):
            writer.print("pass")
            writer.elif_statement("condition 2")
            writer.print("pass")
            writer.else_statement()
            writer.print("pass")

    assert (
        buffer.getvalue()
        == """\
class ClassA(int, str):
    def __init__(self) -> None:
        pass
     
 
class ClassB:
    pass
 
def main():
    if condition 1:
        pass
    elif condition 2:
        pass
    else:
        pass
 
"""
    )
