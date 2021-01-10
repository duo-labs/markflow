from markflow.formatters.code_block import MarkdownCodeBlock

from .util import create_section, render


class TestCodeBlock:
    def test_backtick(self) -> None:
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

    def test_tilda(self) -> None:
        input_ = (
            "~~~~python   \n"
            "# Very powerful spell   \n"
            "if necromancer:   \n"
            "    raise Dead()  \n"
            "```\n"
            "~~~~"
        )
        expected = (
            "~~~~python\n"
            "# Very powerful spell\n"
            "if necromancer:\n"
            "    raise Dead()\n"
            "```\n"
            "~~~~"
        )
        code_block = create_section(MarkdownCodeBlock, input_)
        assert code_block.reformatted() == expected
        code_block = create_section(MarkdownCodeBlock, expected)
        assert code_block.reformatted() == expected
        assert render(expected) == render(input_)
