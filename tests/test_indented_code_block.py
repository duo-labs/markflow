from markflow.formatters.indented_code_block import MarkdownIndentedCodeBlock

from .util import create_section, render


class TestIndentedCodeBlock:
    def test_simple(self) -> None:
        input_ = "    import goods    \n" "\n" "    tariffs = good.audit()   \n"
        expected = "    import goods\n" "\n" "    tariffs = good.audit()"
        code_block = create_section(MarkdownIndentedCodeBlock, input_)
        assert code_block.reformatted() == expected
        code_block = create_section(MarkdownIndentedCodeBlock, expected)
        assert code_block.reformatted() == expected
        assert render(expected) == render(input_)
