import math

from markflow.formatters.horizontal_line import MarkdownHorizontalLine

from .util import create_section, render


class TestHorizontalLine:
    def test_too_short(self) -> None:
        width = 50
        input_ = "---"
        expected = "-" * width
        h_line = create_section(MarkdownHorizontalLine, input_)
        assert h_line.reformatted(width) == expected
        assert render(expected) == render(input_)

    def test_too_long(self) -> None:
        width = 50
        input_ = "-" * 100
        expected = "-" * width
        h_line = create_section(MarkdownHorizontalLine, input_)
        assert h_line.reformatted(width) == expected
        assert render(expected) == render(input_)

    def test_infinity(self) -> None:
        width = math.inf
        input_ = "----------"
        expected = "---"
        h_line = create_section(MarkdownHorizontalLine, input_)
        assert h_line.reformatted(width) == expected
        assert render(expected) == render(input_)
