from markflow.formatters.code_block import MarkdownCodeBlock

from .util import create_section, render


class TestIndentedCodeBlock:
    def test_simple(self) -> None:
        input_ = "    import goods    \n" "\n" "    tariffs = good.audit()   \n"
        expected = "    import goods\n" "\n" "    tariffs = good.audit()"
        code_block = create_section(MarkdownCodeBlock, input_)
        assert code_block.reformatted() == expected
        code_block = create_section(MarkdownCodeBlock, expected)
        assert code_block.reformatted() == expected
        assert render(expected) == render(input_)
