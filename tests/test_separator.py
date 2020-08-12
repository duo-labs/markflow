from markflow.formatters.separator import MarkdownSeparator

from .util import create_section, render


class TestSeparator:
    def test_separator(self) -> None:
        input_ = "  \n\n      \n"
        expected = "\n\n"
        separator = create_section(MarkdownSeparator, input_)
        assert separator.reformatted() == expected
        assert render(expected) == render(input_)
