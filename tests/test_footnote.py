from markflow.formatters.footnote import MarkdownFootnote

from .util import create_section, render


class TestFootnote:
    def test_footnote(self) -> None:
        input_ = (
            "[footnote1]: http://example.com\n"
            "   [footnote2]: http://example.com   \n"
            "  [footnote3]: http://example.com"
        )
        expected = (
            "[footnote1]: http://example.com\n"
            "[footnote2]: http://example.com\n"
            "[footnote3]: http://example.com"
        )
        footnote = create_section(MarkdownFootnote, input_)
        assert footnote.reformatted() == expected
        footnote = create_section(MarkdownFootnote, expected)
        assert footnote.reformatted() == expected
        assert render(expected) == render(input_)
