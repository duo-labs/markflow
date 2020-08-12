import textwrap

from markflow.formatters import MarkdownBlockQuote

# TODO: Apparently rendered HTML cares about blank block quotes
# In retrospect, this kind of spacing is respected in non-block quotes, so we should be
# doing the same.
from .util import create_section, render


class TestBlockQuote:
    def test_basic(self) -> None:
        input_ = textwrap.dedent(
            """\
            > > Double Indented > Quote
            >
            >>
            >Quote \\>
            More Quote
            >>> Triple Indented Quote
            > > Part of that Triple Indented Quote"""
        )
        expected = textwrap.dedent(
            """\
            >> Double Indented \\> Quote
            >
            >>
            > Quote \\> More Quote
            >>> Triple Indented Quote Part of
            >>> that Triple Indented Quote"""
        )
        block_quote = create_section(MarkdownBlockQuote, input_)
        assert block_quote.reformatted(width=35) == expected
        block_quote = create_section(MarkdownBlockQuote, expected)
        assert block_quote.reformatted(width=35) == expected
        assert render(expected) == render(input_)
