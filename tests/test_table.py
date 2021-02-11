import textwrap

from markflow.formatters.table import (
    MarkdownTable,
    center_align,
    left_align,
    right_align,
)

from .util import create_section


class TestAlign:
    def test_center_align(self) -> None:
        assert center_align("a", 3) == " a "
        assert center_align("aa", 3) == "aa "
        assert center_align("aa", 4) == " aa "

    def test_left_align(self) -> None:
        assert left_align("a", 3) == "a  "
        assert left_align("aa", 3) == "aa "
        assert left_align("aa", 4) == "aa  "

    def test_right_align(self) -> None:
        assert right_align("a", 3) == "  a"
        assert right_align("aa", 3) == " aa"
        assert right_align("aa", 4) == "  aa"


class TestTable:
    def test_table(self) -> None:
        input_ = textwrap.dedent(
            """\
            |Heading 1|Heading 2|
            |--|--|
            |Short|Very long even line|
            |Very long odd line|Short|"""
        )
        expected = textwrap.dedent(
            """\
            |     Heading 1      |      Heading 2      |
            |--------------------|---------------------|
            | Short              | Very long even line |
            | Very long odd line | Short               |"""
        )
        table = create_section(MarkdownTable, input_)
        assert table.reformatted() == expected
        table = create_section(MarkdownTable, expected)
        assert table.reformatted() == expected

    def test_aligned_table(self) -> None:
        input_ = textwrap.dedent(
            """\
            | L | C | R |
            |:--|:-:|--:|
            | a | a | a|
            |abcde | abcde|abcde|"""
        )
        expected = textwrap.dedent(
            """\
            | L     |   C   |     R |
            |:------|:-----:|------:|
            | a     |   a   |     a |
            | abcde | abcde | abcde |"""
        )
        table = create_section(MarkdownTable, input_)
        assert table.reformatted() == expected
        table = create_section(MarkdownTable, expected)
        assert table.reformatted() == expected
