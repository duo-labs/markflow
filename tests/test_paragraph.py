import textwrap

from mdformat.formatters.paragraph import MarkdownParagraph

from .util import create_section, render


class TestParagraph:
    def test_paragraph(self) -> None:
        input_ = (
            "This is a test string. It must have a [footnote][footnote] that breaks "
            "across a line and a [URL](http://example.com) so we can ensure that we "
            "get good coverage."
        )
        expected = textwrap.dedent(
            """\
            This is a test string. It must have a [footnote][
            footnote] that breaks across a line and a [URL](
            http://example.com) so we can ensure that we get
            good coverage."""
        )
        paragraph = create_section(MarkdownParagraph, input_)
        assert paragraph.reformatted(width=50) == expected
        paragraph = create_section(MarkdownParagraph, expected)
        assert paragraph.reformatted(width=50) == expected
        assert render(expected) == render(input_)

    def test_hyperlink_breaking(self) -> None:
        input_ = textwrap.dedent(
            """\
            [I'm a hyperlink broken across multiple lines.](
            test.htm)"""
        )
        expected = "[I'm a hyperlink broken across multiple lines.](test.htm)"
        paragraph = create_section(MarkdownParagraph, input_)
        assert paragraph.reformatted() == expected
        paragraph = create_section(MarkdownParagraph, expected)
        assert paragraph.reformatted() == expected
        assert render(expected) == render(input_)
