import math

from markflow.formatters.thematic_break import MarkdownThematicBreak

from .util import create_section, render


class TestThematicBreak:
    def test_too_short(self) -> None:
        width = 50
        input_ = "---"
        expected = "-" * width
        h_line = create_section(MarkdownThematicBreak, input_)
        assert h_line.reformatted(width) == expected
        assert render(expected) == render(input_)

    def test_too_long(self) -> None:
        width = 50
        input_ = "-" * 100
        expected = "-" * width
        h_line = create_section(MarkdownThematicBreak, input_)
        assert h_line.reformatted(width) == expected
        assert render(expected) == render(input_)

    def test_infinity(self) -> None:
        width = math.inf
        input_ = "----------"
        expected = "---"
        h_line = create_section(MarkdownThematicBreak, input_)
        assert h_line.reformatted(width) == expected
        assert render(expected) == render(input_)
