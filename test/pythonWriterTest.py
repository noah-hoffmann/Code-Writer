from CodeWriter import PythonWriter


def main():
    writer = PythonWriter()
    with writer.new_class("MyClass"):
        with writer.function("__init__", "self"):
            writer.print("pass")
    with writer.new_class("Child", "MyClass"):
        with writer.function("__init__", "self", "x"):
            writer.print("pass")
    with writer.function("main"):
        writer.print("x = 0")
        with writer.range_loop("i", "10"):
            with writer.if_statement("i % 2 == 0"):
                writer.print("x += i")
                writer.else_statement()
                writer.print("x -= i")
        writer.print("return x")
    with writer.if_statement("__name__ == '__main__'"):
        writer.print("main()")


if __name__ == '__main__':
    main()
