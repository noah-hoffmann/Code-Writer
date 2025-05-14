from CodeWriter import LatexWriter


def main():
    writer = LatexWriter()

    with writer.environment("document"):
        writer.print("Some Text. \nBla Bla")
        with writer.itemize():
            writer.item("Item 1")
            writer.item("Item 2")
            with writer.environment("tikzpicture"):
                writer.print(r"\draw something")
                writer.print(r"\draw something else")
            writer.item("Item 3")
            writer.print("Some text to item 3")
        writer.print("Goodbye!")


if __name__ == "__main__":
    main()
