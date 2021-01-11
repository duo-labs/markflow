from markflow.formatters.link_reference_definition import (
    MarkdownLinkReferenceDefinition,
)

from .util import create_section, render


class TestLinkReferenceDefinition:
    # TODO: Port footnotes from file 0007 to here
    def test_basic(self) -> None:
        input_ = "   [footnote1]: http://example.com     "
        expected = "[footnote1]: http://example.com"
        footnote = create_section(MarkdownLinkReferenceDefinition, input_)
        assert footnote.reformatted() == expected
        footnote = create_section(MarkdownLinkReferenceDefinition, expected)
        assert footnote.reformatted() == expected
        assert render(expected) == render(input_)
