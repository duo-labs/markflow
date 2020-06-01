import textwrap

from mdformat.formatters.list import MarkdownList, split_code

import pytest

from .util import create_section, render


class TestSplitCode:
    def test_nosplit(self) -> None:
        input_ = """\
        test
        test"""
        expected = [input_]
        assert split_code(input_) == expected

    def test_split(self) -> None:
        input_ = textwrap.dedent(
            """\
            plaintext
            ```
            code
            code
            ```
            plaintext"""
        )
        expected = ["plaintext", "```\ncode\ncode\n```", "plaintext"]
        assert split_code(input_) == expected


class TestMarkdownList:
    def test_basic(self) -> None:
        input_ = textwrap.dedent(
            """\
            * I am a list that is pretty badly
            formatted
            * There are all sorts of problems that don't make this look very nice, like
            bullets that break across lines and missing spaces.
            * Which also is a problem when working with nested lists since they could be
            missing leading spaces and make things look extra confusing."""
        )
        expected = textwrap.dedent(
            """\
            * I am a list that is pretty badly formatted
            * There are all sorts of problems that don't make
              this look very nice, like bullets that break
              across lines and missing spaces.
            * Which also is a problem when working with nested
              lists since they could be missing leading spaces
              and make things look extra confusing."""
        )
        lst = create_section(MarkdownList, input_)
        assert lst.reformatted(width=50) == expected
        lst = create_section(MarkdownList, expected)
        assert lst.reformatted(width=50) == expected
        assert render(expected) == render(input_)

    def test_make_bullets_same(self) -> None:
        input_ = textwrap.dedent(
            """\
            * Test
            + Test
            - Test"""
        )
        expected = textwrap.dedent(
            """\
            * Test
            * Test
            * Test"""
        )
        lst = create_section(MarkdownList, input_)
        assert lst.reformatted() == expected
        lst = create_section(MarkdownList, expected)
        assert lst.reformatted() == expected
        # Since we correct lists that have mismatched indicators, we update the strings
        # to have consistent bullets.
        # Note: Here, this doesn't actually test much. We keep it here for test
        #       consistency.
        input_ = input_.replace("-", "*").replace("+", "*")
        expected = expected.replace("-", "*").replace("+", "*")
        assert render(expected) == render(input_)

    def test_correct_numbering(self) -> None:
        input_ = textwrap.dedent(
            """\
            1. Test
            1. Test
            4. Test"""
        )
        expected = textwrap.dedent(
            """\
            1. Test
            2. Test
            3. Test"""
        )
        lst = create_section(MarkdownList, input_)
        assert lst.reformatted() == expected
        lst = create_section(MarkdownList, expected)
        assert lst.reformatted() == expected
        assert render(expected) == render(input_)

    def test_nested_unordered(self) -> None:
        input_ = textwrap.dedent(
            """\
            * This is a really long line that with terrible
            spacing
              - This is also a really long line with terrible
            spacing
              * This one's ok though
            - So is this one"""
        )
        expected = textwrap.dedent(
            """\
            * This is a really long line that with terrible
              spacing
              - This is also a really long line with terrible
                spacing
              - This one's ok though
            * So is this one"""
        )
        lst = create_section(MarkdownList, input_)
        assert lst.reformatted(width=50) == expected
        lst = create_section(MarkdownList, expected)
        assert lst.reformatted(width=50) == expected
        # Since we correct lists that have mismatched indicators, we update the strings
        # to have consistent bullets.
        input_ = input_.replace("-", "*")
        expected = expected.replace("-", "*")
        assert render(expected) == render(input_)

    def test_nested_ordered(self) -> None:
        input_ = textwrap.dedent(
            """\
            1. This is a really long line that with terrible
            spacing
               1. This is also a really long line with terrible
            spacing
               1. This one's ok though
               1. This one isn't
            great
            1. So is this one"""
        )
        expected = textwrap.dedent(
            """\
            1. This is a really long line that with terrible
               spacing
               1. This is also a really long line with
                  terrible spacing
               2. This one's ok though
               3. This one isn't great
            2. So is this one"""
        )
        lst = create_section(MarkdownList, input_)
        assert lst.reformatted(width=50) == expected
        lst = create_section(MarkdownList, expected)
        assert lst.reformatted(width=50) == expected
        input_ = input_.replace("-", "*")
        expected = expected.replace("-", "*")
        assert render(expected) == render(input_)

    def test_weird_indenting(self) -> None:
        input_ = textwrap.dedent(
            """\
            * This is a really long line that with terrible
            spacing
                 * Let's make sure this doesn't stay here
              * This is also a really long line with terrible
            spacing
                 - Let's make sure this does stay here
              - This one's ok though, minus the symbol
            - So is this one"""
        )
        expected = textwrap.dedent(
            """\
            * This is a really long line that with terrible
              spacing
              * Let's make sure this doesn't stay here
              * This is also a really long line with terrible
                spacing
                - Let's make sure this does stay here
              * This one's ok though, minus the symbol
            * So is this one"""
        )
        lst = create_section(MarkdownList, input_)
        assert lst.reformatted(width=50) == expected
        lst = create_section(MarkdownList, expected)
        assert lst.reformatted(width=50) == expected
        # Since we correct lists that have mismatched indicators, we update the strings
        # to have consistent bullets.
        input_ = input_.replace("-", "*")
        expected = expected.replace("-", "*")
        assert render(expected) == render(input_)

    def test_links(self) -> None:
        input_ = textwrap.dedent(
            """\
            * [URL](http://example.com/very/nested/directory)
            * [URL](http://example.com)"""
        )
        expected = textwrap.dedent(
            """\
            * [URL](
              http://example.com/very/nested/directory)
            * [URL](http://example.com)"""
        )
        lst = create_section(MarkdownList, input_)
        assert lst.reformatted(width=30) == expected
        lst = create_section(MarkdownList, expected)
        assert lst.reformatted(width=30) == expected
        assert render(expected) == render(input_)

    def test_indented(self) -> None:
        input_ = "  * Entry 1\n* Entry 2"
        expected = "  * Entry 1\n  * Entry 2"
        lst = create_section(MarkdownList, input_)
        assert lst.reformatted() == expected
        lst = create_section(MarkdownList, expected)
        assert lst.reformatted() == expected
        assert render(expected) == render(input_)

    def test_indented_numerics(self) -> None:
        input_ = "  1. Test\n  2. Test\n 10. Test"
        expected = " 1. Test\n 2. Test\n 3. Test"
        lst = create_section(MarkdownList, input_)
        assert lst.reformatted() == expected
        lst = create_section(MarkdownList, expected)
        assert lst.reformatted() == expected
        assert render(expected) == render(input_)

    def test_ordered_list_with_nine_entries(self) -> None:
        """Ensure we don't add extra indents on 10^n-1 length lists"""
        input_ = (
            "1. a\n"
            "2. b\n"
            "3. c\n"
            "4. d\n"
            "5. e\n"
            "6. f\n"
            "7. g\n"
            "8. h\n"
            "9. i"
        )
        expected = input_
        lst = create_section(MarkdownList, input_)
        assert lst.reformatted() == expected
        lst = create_section(MarkdownList, expected)
        assert lst.reformatted() == expected
        assert render(expected) == render(input_)

    @pytest.mark.xfail(
        reason="TODO: Indentation isn't properly detected with ordered lists."
    )
    def test_nested_ordered_bad_indent(self) -> None:
        input_ = textwrap.dedent(
            """\
            1. This is a really long line that with terrible
            spacing
              1. This is also a really long line with terrible
            spacing
              1. This one's ok though
              1. This one isn't
            great
            1. So is this one"""
        )
        expected = textwrap.dedent(
            """\
            1. This is a really long line that with terrible
               spacing
            2. This is also a really long line with terrible
               spacing
            3. This one's ok though
            4. This one isn't great
            5. So is this one"""
        )
        lst = create_section(MarkdownList, input_)
        assert lst.reformatted(width=50) == expected
        lst = create_section(MarkdownList, expected)
        assert lst.reformatted(width=50) == expected
        input_ = input_.replace("-", "*")
        expected = expected.replace("-", "*")
        assert render(expected) == render(input_)
