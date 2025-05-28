from io import StringIO

from CodeWriter import FortranWriter


def test_FortranWriter():
    buffer = StringIO()
    writer = FortranWriter(file=buffer)

    writer.comment(
        """\
        This module was generated automatically.
        Do not change it!"""
    )
    with writer.module("my_module"):
        writer.use("constants, only: pi")
        writer.print("implicit none")
        writer.contains()
        with writer.function(
            "my_func", "arg1", "arg2", result="result", elemental=True, pure=True
        ):
            writer.declare("real", "arg1", "arg2", intent="in")
            writer.declare("real, allocatable, dimensions(:)", "result", intent="out")
            writer.print()
        with writer.subroutine("my_routine", "arg1", "arg2"):
            with writer.if_then("condition"):
                writer.comment("Do Stuff")
            with writer.select("var"):
                writer.case("case 1")
                writer.comment("Case 1 Stuff")
                writer.item("default")
                writer.comment("Default Stuff")
    assert (
        buffer.getvalue()
        == """\
! This module was generated automatically.
! Do not change it!
module my_module
    use constants, only: pi
    implicit none
contains
    elemental function my_func(arg1, arg2) result(result)
        real, intent(in) :: arg1, arg2
        real, allocatable, dimensions(:), intent(out) :: result
        
    end function my_func
        
    subroutine my_routine(arg1, arg2)
        if (condition) then
            ! Do Stuff
        end if
        select case (var)
            case (case 1)
                ! Case 1 Stuff
            case default
                ! Default Stuff
        end select
    end subroutine my_routine
        
end module my_module
"""
    )
