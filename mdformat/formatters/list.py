import enum
import itertools
import re

from typing import List
from ..typing import Number, SectionEndedFunc

from ..detectors.code_block import (
    create_code_block_ended_func,
    tilda_code_block_started,
)

from .base import MarkdownSection
from .textwrap import wrap

__all__ = ["MarkdownList"]

MARKER_REGEX = re.compile(
    r"^\s*"  # Leading spaces are allowed and often expected
    r"("
    r"\*|"  # Asterisk list marker
    r"-|"  # Dash list marker
    r"\+|"  # Plus list marker
    r"[0-9]+\."  # Numeric list marker
    r") "
)


class ListTypes(enum.Enum):
    ASTERISK = "*"
    DASH = "-"
    NUMERIC = "no."
    PLUS = "+"


def split_code(text: str) -> List[str]:
    """ Splits text into a list of alternating plaintext and code sections

    Calls in this file can take advantage of the face that this will always get called
    with text that starts with plaintext.
    """
    sections: List[str] = []
    in_code_block = False
    code_block_ended_function: SectionEndedFunc = lambda _line, _i, _lines: False
    lines = text.splitlines()
    for index, line in enumerate(lines):
        was_in_code_block = in_code_block
        if in_code_block:
            if code_block_ended_function(line, index, lines):
                in_code_block = False
        if not in_code_block:
            if tilda_code_block_started(line, index, lines):
                in_code_block = True
                code_block_ended_function = create_code_block_ended_func(
                    line, index, lines
                )
        switched = was_in_code_block != in_code_block

        if switched or not sections:
            sections.append(line)
        else:
            sections[-1] += "\n" + line

    return sections


class MarkdownList(MarkdownSection):
    def append(self, line: str) -> None:
        self.lines.append(line)

    def reformatted(self, width: Number = 88) -> str:
        entries: List[str] = []
        sections = split_code("\n".join(self.lines))
        for section, is_code in zip(sections, itertools.cycle([False, True])):
            if is_code:
                entries[-1] += "\n" + section + "\n"
            else:
                for line in section.splitlines():
                    if MARKER_REGEX.search(line):
                        entries.append(line.rstrip())
                    else:
                        if not entries[-1].endswith("-"):
                            entries[-1] += " "
                        entries[-1] += line.rstrip()
        # Remove trailing new lines from code sections
        entries = [entry.rstrip() for entry in entries]

        first_space = len(entries[0]) - len(entries[0].lstrip())
        # Keeps track of at what spacing each level of the stack was detected at.
        space_stack = [first_space]
        depths = [0]

        # Calculate the depth of each level in our list where 0 is the lowest level
        # This is further complicated by the fact that the following, has only two
        # levels:
        # * Level 0
        #     * Level 1
        #   * Level 1
        # At least according to every markdown renderer I have used.
        for entry in entries[1:]:
            space = len(entry) - len(entry.lstrip())
            if space > space_stack[-1]:
                space_stack.append(space)
            elif space == space_stack[-1]:
                pass
            else:
                for entry_depth, space_to_check in enumerate(space_stack):
                    if space > space_to_check:
                        continue
                    else:
                        new_space_stack = []
                        for i in range(entry_depth):
                            new_space_stack.append(space_stack[i])
                        new_space_stack.append(space)
                        space_stack = new_space_stack
                        break
            depths.append(len(space_stack) - 1)

        for prev_depth, current_depth in zip([0] + depths, depths):
            if not current_depth <= prev_depth + 1:
                raise RuntimeError(
                    f"Incorrect depth calculation. Consecutive depths were calculated "
                    f"as {prev_depth}, {current_depth}. Depths should increase by at "
                    f"most one for consecutive entries"
                )

        # Go through our entries and ensure subsections all have matching markers and
        # numbered lists use proper numbers
        canonicalized_depths: List[int] = []
        new_entries = [""] * len(entries)
        total_indent = 0
        for index, (entry, depth) in enumerate(zip(entries, depths)):
            # Remove subsection depths we've left behind
            canonicalized_depths = [
                d for i, d in zip(range(depth + 1), canonicalized_depths)
            ]

            if depth in canonicalized_depths:
                continue

            # Find all entries part of our current subsection
            relevant_indexes = []
            for offset, (entry_to_check, depth_to_check) in enumerate(
                zip(entries[index:], depths[index:])
            ):
                if depth_to_check == depth:
                    relevant_indexes.append(index + offset)
                elif depth_to_check < depth:
                    break

            if entries[relevant_indexes[0]].lstrip().startswith("*"):
                type = ListTypes.ASTERISK
            elif entries[relevant_indexes[0]].lstrip().startswith("-"):
                type = ListTypes.DASH
            elif entries[relevant_indexes[0]].lstrip().startswith("+"):
                type = ListTypes.PLUS
            else:
                type = ListTypes.NUMERIC

            if type == ListTypes.NUMERIC:
                max_number_len = len(str(len(relevant_indexes)))
                max_marker_len = 0
                for entry_number, entry_index in enumerate(relevant_indexes, start=1):
                    marker, entry_text = (
                        entries[entry_index].lstrip().split(" ", maxsplit=1)
                    )
                    max_marker_len = max(len(marker), max_marker_len)
                    entry_text = entry_text.lstrip()
                    leading_space = " " * (max_number_len - len(str(entry_number)))
                    prefix = f"{leading_space}{entry_number}. "
                    entry_text = prefix + entry_text
                    new_entries[entry_index] = entry_text

                if index == 0:
                    first_indent = len(entries[0]) - len(entries[0].lstrip())
                    # Subtract 3 for the period and the fact that our first numeric, 1,
                    # has a length of 1
                    first_indent -= max_marker_len - 2
                    total_indent = max(0, first_indent)
            else:
                if type == ListTypes.ASTERISK:
                    prefix = "* "
                else:
                    prefix = "- "
                for entry_index in relevant_indexes:
                    entry_text = (
                        entries[entry_index].lstrip().split(" ", maxsplit=1)[1].lstrip()
                    )
                    entry_text = prefix + entry_text
                    new_entries[entry_index] = entry_text

                if index == 0:
                    total_indent = len(entries[0]) - len(entries[0].lstrip())

            canonicalized_depths.append(depth)

        entries = new_entries

        # How much more the text of each depth entry was indented compared to the one
        # before it
        indent_lengths: List[int] = []
        new_entries = []
        for entry, depth in zip(entries, depths):
            # Remove indents from subsections we are no longer in
            indent_lengths = [d for i, d in zip(range(depth + 1), indent_lengths)]
            marker_match = MARKER_REGEX.match(entry)
            if marker_match is None:
                raise RuntimeError(
                    "List identification resulted in an entry without a marker."
                )
            if len(indent_lengths) != depth + 1:
                indent_lengths.append(len(marker_match.group()))
            entry_text = entry[marker_match.end() :]  # noqa: E203
            entry_indent = total_indent + sum(indent_lengths[:-1])
            text_indent = total_indent + sum(indent_lengths)

            # To output the text, we wrap the plaintext and leave the lines alone.
            output_text = ""
            for section, is_code in zip(
                split_code(entry_text), itertools.cycle([False, True])
            ):
                if is_code:
                    output_text += "\n" + section + "\n"
                else:
                    wrapped_text = wrap(section, width - text_indent)
                    indented_text = ("\n" + " " * text_indent).join(
                        wrapped_text.splitlines()
                    )
                    if output_text:
                        output_text += " " * text_indent
                    else:
                        output_text += " " * entry_indent + marker_match.group()
                    output_text += indented_text
            new_entries.append(output_text.rstrip())

        return "\n".join(new_entries)
