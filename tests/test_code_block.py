from mdformat.formatters.code_block import MarkdownCodeBlock

from .util import create_section, render


class TestCodeBlock:
    def test_tilda_code_block(self) -> None:
        input_ = (
            "```python   \n"
            "# Very powerful spell   \n"
            "if necromancer:   \n"
            "    raise Dead()  \n"
            "```"
        )
        expected = (
            "```python\n"
            "# Very powerful spell\n"
            "if necromancer:\n"
            "    raise Dead()\n"
            "```"
        )
        code_block = create_section(MarkdownCodeBlock, input_)
        assert code_block.reformatted() == expected
        code_block = create_section(MarkdownCodeBlock, expected)
        assert code_block.reformatted() == expected
        assert render(expected) == render(input_)

    def test_indented_code_block(self) -> None:
        input_ = "    import goods    \n" "\n" "    tariffs = good.audit()   \n"
        expected = "    import goods\n" "\n" "    tariffs = good.audit()"
        code_block = create_section(MarkdownCodeBlock, input_)
        assert code_block.reformatted() == expected
        code_block = create_section(MarkdownCodeBlock, expected)
        assert code_block.reformatted() == expected
        assert render(expected) == render(input_)
