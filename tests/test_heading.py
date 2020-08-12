from markflow.formatters.heading import MarkdownHeading

from .util import create_section, render


class TestHeading:
    def test_octothorpe_heading(self) -> None:
        input_ = "   # Heading    "
        expected = "# Heading"
        heading = create_section(MarkdownHeading, input_)
        assert heading.reformatted() == expected
        heading = create_section(MarkdownHeading, expected)
        assert heading.reformatted() == expected
        assert render(expected) == render(input_)

    def test_underlined_heading(self) -> None:
        input_ = "   Heading    \n---"
        expected = "Heading\n-------"
        heading = create_section(MarkdownHeading, input_)
        assert heading.reformatted() == expected
        heading = create_section(MarkdownHeading, expected)
        assert heading.reformatted() == expected
        assert render(expected) == render(input_)

    def test_single_character_underlined_heading(self) -> None:
        input_ = "A\n----"
        expected = "A\n-"
        heading = create_section(MarkdownHeading, input_)
        assert heading.reformatted() == expected
        heading = create_section(MarkdownHeading, expected)
        assert heading.reformatted() == expected
        assert render(expected) == render(input_)
