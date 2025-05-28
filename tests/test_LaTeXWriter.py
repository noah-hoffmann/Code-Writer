from io import StringIO

from CodeWriter import LatexWriter


def test_LatexWriter():
    buffer = StringIO()
    writer = LatexWriter(file=buffer)
    writer.print(r"\include{package}")
    with writer.environment("document"):
        writer.print("Hello, World!")
        with writer.itemize(label="alpha"):
            writer.item("Item 1")
            writer.print("Some text!")
        with writer.enumerate():
            writer.item("Item 1")
        with writer.environment("environment", "required", "optional"):
            pass
        with writer.environment("environment", "required"):
            pass
        with writer.environment("environment", optional="optional"):
            pass
    buffer.getvalue() == r"""\
\begin{document}
    Hello, World!
    \begin{itemize}[label=alpha]
        \item Item 1
            Some text!
    \end{itemize}
    \begin{enumerate}
        \item Item 1
    \end{enumerate}
    \begin{environment}[optional]{required}
    \end{environment}
    \begin{environment}{required}
    \end{environment}
    \begin{environment}[optional]
    \end{environment}
\end{document}
"""
