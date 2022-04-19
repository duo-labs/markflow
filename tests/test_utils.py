import textwrap

from markflow._utils._utils import get_indent, truncate_str
from markflow._utils.textwrap import (
    code_split,
    link_split,
    newline_split,
    space_split,
    wrap,
)


class TestTruncateStr:
    def test_shorter(self) -> None:
        assert truncate_str("123456789", 19) == "123456789"

    def test_exact_length(self) -> None:
        assert truncate_str("123456789", 9) == "123456789"

    def test_longer(self) -> None:
        assert truncate_str("123456789", 5) == "12..."

    def test_truncate_less_than_ellipsis(self) -> None:
        assert truncate_str("123456789", 2) == ".."


class TestGetIndent:
    def test_is_indented_at_least(self) -> None:
        # This is a little silly, but I expect we may have more cases to support since
        # we currently conflate tabs and spaces.
        assert get_indent("  Test") == 2


class TestTextWrap:
    def test_all_splits(self) -> None:
        input_ = (
            "abc abc abc abc abc abc abc abc abc ``abc ``` abc[0][0] ``abc abc abc abc "
            "<br /><br /> abc abc [url](http://example.com) "
            "abc[url][http://example.com]abc[url][URL][url][URL]  <br/>abc<br/>"
        )
        expected = textwrap.dedent(
            """\
            abc abc abc abc abc abc abc abc abc
            ``abc ``` abc[0][0] ``abc abc abc abc <br />
            <br />
            abc abc [url](http://example.com)abc[url][
            http://example.com]abc[url][URL][url][URL] <br/>
            abc<br/>"""
        )
        assert wrap(input_, 50) == expected

    def test_code_split(self) -> None:
        input_ = "a` a `` b` a `b`c"
        expected_split_text = ["a", "` a `` b`", "a", "`b`", "c"]
        expected_leading_spaces = [False, False, True, True, False]
        expected_evaluates = [True, False, True, False, True]
        split_text, leading_spaces, evaluates = code_split(input_, False)
        assert len(split_text) == len(leading_spaces) == len(evaluates)
        assert split_text == expected_split_text
        assert leading_spaces == expected_leading_spaces
        assert evaluates == expected_evaluates

    def test_code_split_begin_and_end(self) -> None:
        input_ = "` a `` b` a `b`"
        expected_split_text = ["` a `` b`", "a", "`b`"]
        expected_leading_spaces = [False, True, True]
        expected_evaluates = [False, True, False]
        split_text, leading_spaces, evaluates = code_split(input_, False)
        assert len(split_text) == len(leading_spaces) == len(evaluates)
        assert split_text == expected_split_text
        assert leading_spaces == expected_leading_spaces
        assert evaluates == expected_evaluates

    def test_code_split_sentence(self) -> None:
        input_ = "a` a `` b`. a `b`.c"
        expected_split_text = ["a", "` a `` b`.", "a", "`b`.", "c"]
        expected_leading_spaces = [False, False, True, True, False]
        expected_evaluates = [True, False, True, False, True]
        split_text, leading_spaces, evaluates = code_split(input_, False)
        assert len(split_text) == len(leading_spaces) == len(evaluates)
        assert split_text == expected_split_text
        assert leading_spaces == expected_leading_spaces
        assert evaluates == expected_evaluates

    def test_code_split_solo_tilda(self) -> None:
        input_ = "` a `` b` a `b` `a"
        expected_split_text = ["` a `` b`", "a", "`b`", "`a"]
        expected_leading_spaces = [False, True, True, True]
        expected_evaluates = [False, True, False, True]
        split_text, leading_spaces, evaluates = code_split(input_, False)
        assert len(split_text) == len(leading_spaces) == len(evaluates)
        assert split_text == expected_split_text
        assert leading_spaces == expected_leading_spaces
        assert evaluates == expected_evaluates

    def test_link_split(self) -> None:
        input_ = "a[URL][url] b [URL](http://example.com)c"
        expected_split_text = [
            "a[URL][",
            "url]",
            "b",
            "[URL](",
            "http://example.com)c",
        ]
        expected_leading_spaces = [False, False, True, True, False]
        expected_evaluates = [True, False, True, True, False]
        split_text, leading_spaces, evaluates = link_split(input_, False)
        assert len(split_text) == len(leading_spaces) == len(evaluates)
        assert split_text == expected_split_text
        assert leading_spaces == expected_leading_spaces
        assert evaluates == expected_evaluates

    def test_link_split_sentence(self) -> None:
        input_ = "a[URL][url]. b [URL](http://example.com).c"
        expected_split_text = [
            "a[URL][",
            "url].",
            "b",
            "[URL](",
            "http://example.com).c",
        ]
        expected_leading_spaces = [False, False, True, True, False]
        expected_evaluates = [True, False, True, True, False]
        split_text, leading_spaces, evaluates = link_split(input_, False)
        assert len(split_text) == len(leading_spaces) == len(evaluates)
        assert split_text == expected_split_text
        assert leading_spaces == expected_leading_spaces
        assert evaluates == expected_evaluates

    def test_newline_split(self) -> None:
        input_ = "a <br /> b <br>c<br/>d"
        expected_split_text = ["a", "<br />", "b", "<br>", "c", "<br/>", "d"]
        expected_leading_spaces = [False, True, True, True, False, False, False]
        expected_evaluates = [True, False, True, False, True, False, True]
        split_text, leading_spaces, evaluates = newline_split(input_, False)
        assert len(split_text) == len(leading_spaces) == len(evaluates)
        assert split_text == expected_split_text
        assert leading_spaces == expected_leading_spaces
        assert evaluates == expected_evaluates

    def test_space_split(self) -> None:
        input_ = " ".join(["a"] * 10)
        expected_split_text = ["a"] * 10
        expected_leading_spaces = [False] + [True] * 9
        expected_evaluates = [True] * 10
        split_text, leading_spaces, evaluates = space_split(input_, False)
        assert len(split_text) == len(leading_spaces) == len(evaluates)
        assert split_text == expected_split_text
        assert leading_spaces == expected_leading_spaces
        assert evaluates == expected_evaluates
