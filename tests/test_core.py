from io import StringIO
from CodeWriter import Writer


def test_writer():
    buffer = StringIO()
    writer = Writer(indentation=" " * 2, file=buffer)

    writer.print("Line 1")
    writer.print("Line 2")
    with writer.block("BEGIN BLOCK", "END BLOCK"):
        writer.print("Line 3\nLine 4")
        with writer.listing("BEGIN LISTING", "ITEM", "END LISTING"):
            writer.item("item 1")
            writer.item("item 2")

    string = buffer.getvalue()
    assert (
        string
        == """\
Line 1
Line 2
BEGIN BLOCK
  Line 3
  Line 4
  BEGIN LISTING
    ITEM item 1
    ITEM item 2
  END LISTING
END BLOCK
"""
    )
