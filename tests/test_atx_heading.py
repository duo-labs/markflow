from markflow.formatters.atx_heading import MarkdownATXHeading

from .util import create_section, render


class TestATXHeading:
    def test_simple(self) -> None:
        input_ = "   # Heading    "
        expected = "# Heading"
        atx_heading = create_section(MarkdownATXHeading, input_)
        assert atx_heading.reformatted() == expected
        atx_heading = create_section(MarkdownATXHeading, expected)
        assert atx_heading.reformatted() == expected
        assert render(expected) == render(input_)

    def test_technically_invalid(self) -> None:
        # The ATX spec doesn't allow for spaces between # and whatever, but we fix that
        # for people.
        input_ = "   #Heading    "
        expected = "# Heading"
        atx_heading = create_section(MarkdownATXHeading, input_)
        assert atx_heading.reformatted() == expected
        # We skip rendering checks because the above is really a paragraph. We're just
        # helping.
