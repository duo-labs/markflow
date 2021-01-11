from markflow.formatters.blank_line import MarkdownBlankLine

from .util import create_section, render


class TestBlankLine:
    def test_simple(self) -> None:
        input_ = "    "
        expected = ""
        separator = create_section(MarkdownBlankLine, input_)
        assert separator.reformatted() == expected
        assert render(expected) == render(input_)
