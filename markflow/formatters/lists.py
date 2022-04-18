# 1. Split the list into entries
# 2. Dedent those entries
# 3. Determine indentation level
# 4. Pass each entry to the formatter
# 5. Combine the resulting output
import re
import string
from typing import List

from .._utils import get_indent, redirect_info_logs_to_debug, truncate_str
from ..typing import Number
from .base import MarkdownSection

MARKER_REGEX = re.compile(
    r"^\s*"  # Leading spaces are allowed and often expected
    r"("
    r"\*|"  # Asterisk list marker
    r"-|"  # Dash list marker
    r"\+|"  # Plus list marker
    r"[0-9]+\."  # Numeric list marker
    r")"
    r"($| )"  # End of line or space
)
CODE_BLOCK_FENCES = "`~"
REPR_CONTENT_LEN = 20


def _reformat_markdown(lines: List[str], width: Number) -> str:
    # Prevents issues from circular imports. Since this module would already be loaded
    # whenever we call this function, we know it's cached.
    from ..reformat_markdown import _reformat_markdown_text

    with redirect_info_logs_to_debug():
        text = _reformat_markdown_text("\n".join(lines) + "\n", width)

    return text


def _list_marker_end_pos(line: str) -> int:
    """Return the number of characters before the end of a list marker

    Note: This does not include the trailing space in the count.

    Args:
        line: The lines to evaluate.

    Returns:
        True if the first line would continue the paragraph. False otherwise.
    """

    match = MARKER_REGEX.match(line)
    if match is None:
        raise RuntimeError(
            "Attempted to find the end of a list marker on a line that doesn't have "
            "one. Please open a bug report or email jholland@duosecurity.com."
        )
    return match.end(1)


def _split_list(lines: List[str]) -> List[List[str]]:
    in_code_block = False
    code_block_end = ""

    list_entries: List[List[str]] = []
    max_indent = _list_marker_end_pos(lines[0])
    for line in lines:
        if any(line.lstrip().startswith(f * 3) for f in CODE_BLOCK_FENCES):
            code_block_symbol = line.lstrip()[0]
            code_block_marker_length = len(line.lstrip()) - len(
                line.lstrip(code_block_symbol)
            )
            code_block_marker = code_block_marker_length * code_block_symbol
            if in_code_block:
                if code_block_end == code_block_marker:
                    in_code_block = False
            else:
                in_code_block = True
                code_block_end = code_block_marker

        if MARKER_REGEX.match(line) and not in_code_block:
            line_indent = get_indent(line)
            list_indent = _list_marker_end_pos(line)
            if line_indent <= max_indent:
                max_indent = list_indent
                list_entries.append([line])
            else:
                list_entries[-1].append(line)
        else:
            list_entries[-1].append(line)
    return list_entries


def _dedent_entries(list_entries: List[List[str]]) -> List[List[str]]:
    # ToDo: Should we handle missing spaces? I don't think so. Think:
    #  *read*
    dedented_entries: List[List[str]] = []
    for entry in list_entries:
        indent = _list_marker_end_pos(entry[0]) + 1
        dedented_entries.append([entry[0][indent:]])
        for line in entry[1:]:
            dedented_entry = line[:indent].lstrip() + line[indent:]
            dedented_entries[-1].append(dedented_entry)
    return dedented_entries


class MarkdownBulletList(MarkdownSection):
    @property
    def marker(self) -> str:
        return self.lines[0].lstrip()[0]

    @property
    def first_line(self) -> str:
        return self.lines[0]

    def append(self, line: str) -> None:
        self.lines.append(line)

    def reformatted(self, width: Number = 88) -> str:
        list_entries = _split_list(self.lines)
        # '* '
        toplevel_indent = 2
        dedented_entries = _dedent_entries(list_entries)

        reformatted_entries: List[str] = []
        for entry in dedented_entries:
            with redirect_info_logs_to_debug():
                reformatted_entry = _reformat_markdown(
                    entry, width - toplevel_indent
                ).rstrip("\n")
            reformatted_entry = (
                self.marker
                + " "
                + ("\n" + toplevel_indent * " ").join(reformatted_entry.split("\n"))
            )
            reformatted_entries.append(reformatted_entry)

        return "\n".join(reformatted_entries)

    def __repr__(self) -> str:
        first_line = self.first_line
        if first_line is not None:
            first_line = truncate_str(first_line, REPR_CONTENT_LEN)
        return (
            f"{self.__class__.__name__}: "
            f"marker={repr(self.marker)}; "
            f"first_line={repr(first_line)}>"
        )


class MarkdownOrderedList(MarkdownSection):
    @property
    def first_number(self) -> int:
        lstripped_line = self.lines[0].lstrip()
        return int(
            lstripped_line[
                : len(lstripped_line) - len(lstripped_line.lstrip(string.digits))
            ]
        )

    @property
    def first_line(self) -> str:
        return self.lines[0]

    def reformatted(self, width: Number = 88) -> str:
        list_entries = _split_list(self.lines)
        # '99. '
        toplevel_indent = len(str(self.first_number + len(list_entries) - 1)) + 2
        dedented_entries = _dedent_entries(list_entries)

        reformatted_entries: List[str] = []
        for entry_number, entry in enumerate(dedented_entries, start=self.first_number):
            with redirect_info_logs_to_debug():
                reformatted_entry = _reformat_markdown(
                    entry, width - toplevel_indent
                ).rstrip("\n")
            reformatted_entry = (
                str(entry_number)
                + ". "
                + ("\n" + toplevel_indent * " ").join(reformatted_entry.split("\n"))
            )
            reformatted_entries.append(reformatted_entry)

        return "\n".join(reformatted_entries)

    def __repr__(self) -> str:
        first_line = self.first_line
        if first_line is not None:
            first_line = truncate_str(first_line, REPR_CONTENT_LEN)
        return (
            f"{self.__class__.__name__}: "
            f"first_number={repr(self.first_number)}; "
            f"first_line={repr(first_line)}>"
        )
