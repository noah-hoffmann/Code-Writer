from CodeWriter.FortranWriter import FortranWriter


def main():
    writer = FortranWriter()
    writer.comment(
        """\
        This module was generate automatically.
        Do not change it!\
        """)
    with writer.module("nonlocal_x"):
        writer.use("precision, only: dp")
        writer.use("constants, only: pi")
        writer.print("implicit none")
        writer.print("private")
        writer.print("public :: nonlocal_ex")
        writer.contains()
        with writer.function("nonlocal_ex", "rho", "grho", result="ex"):
            writer.declare("real (dp)", "rho", "grho", intent="in")
            writer.declare("real (dp)", "ex")
            writer.print()
            writer.print("lda_x = -0.75d0")
            writer.print("ex = lda_x")
        with writer.function("nonlocal_vx", trailing=False, elemental=True):
            writer.print()


if __name__ == '__main__':
    main()
