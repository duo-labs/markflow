import re
from typing import List, Tuple

from .._utils import redirect_info_logs_to_debug
from ._lines import (
    is_explicit_block_quote_line,
    is_setext_underline,
    is_thematic_break_line,
)
from .atx_heading import split_atx_heading
from .blank_line import split_blank_line
from .bullet_list import split_bullet_list
from .fenced_code_block import split_fenced_code_block
from .ordered_list import split_ordered_list
from .table import split_table
from .thematic_break import split_thematic_break

LEADING_QUOTE_MARKER = re.compile(r"^ {0,3}>")


def _is_paragraph_continuation_text(lines: List[str], line_offset: int = 0) -> bool:
    """Indicates whether the first line of lines would continue a paragraph

    This ensures that any valid interrupting section of a paragraph could not result in
    a valid block instead.

    We have a separate definition from the one used in paragraph detection to avoid
    circular imports. This definition assumes the line doesn't start with '>'.

    There is also a bit of a diversion from the spec here. According to the spec, the
    following is a block-quoted paragraph:

        > paragraph
        title
        =====

    or:

        > paragraph title =====

    But, that looks odd, and the definition for paragraph continuation text could easily
    be interpreted to consider that a paragraph and a title. So, we do the same here.
    Given that MarkFlow output should not result in any paragraph continuation lines
    after a block quote, there are no concerns around consistency. In the case of
    trailing equals, e.g.

        > paragraph
        ===

    the caller should detect this as a continuation line. But, if it is dashes, it
    should be detected as a horizontal line.

    There is an open issue on the ambiguity of paragraph continuation text here:
    https://github.com/commonmark/commonmark-spec/issues/675

    Args:
        lines: The lines to evaluate.
        line_offset (optional): The offset into the overall document we are at. This is
            used for reporting errors in the original document.

    Returns:
        True if the first line would continue the paragraph. False otherwise.
    """
    from .setext_heading import split_setext_heading

    for splitter in [
        split_atx_heading,
        split_blank_line,
        split_bullet_list,
        split_fenced_code_block,
        split_ordered_list,
        split_setext_heading,
        split_table,
        split_thematic_break,
    ]:
        with redirect_info_logs_to_debug():
            if splitter(lines, line_offset)[0]:
                return False
    if is_setext_underline(lines[0]):
        return False
    return True


def _block_quote_ends_with_paragraph(block_quote_lines: List[str]) -> bool:
    # Avoid circular imports
    from ..parser import MarkdownSectionEnum, parse_markdown

    parsing_lines = []
    for line in block_quote_lines:
        parsing_lines.append(LEADING_QUOTE_MARKER.sub("", line))

    with redirect_info_logs_to_debug():
        ending_section_type, ending_section_content = parse_markdown(parsing_lines)[-1]

    if ending_section_type == MarkdownSectionEnum.BLOCK_QUOTE:
        return _block_quote_ends_with_paragraph(ending_section_content)
    elif ending_section_type == MarkdownSectionEnum.PARAGRAPH:
        return True
    else:
        return False


def split_block_quote(
    lines: List[str], line_offset: int = 0
) -> Tuple[List[str], List[str]]:
    """Splits a block quote from the beginning of lines if one exists

    We slightly differ from the spec when it comes to paragraph continuation lines.
    While the spec detects the following as all a block quoted paragraph:

        > code
        TITLE
        =====

    we detect it as a block quote followed by a heading. In all other ways, we should
    match the spec.

    ToDo:
        * This pattern could be applicable in paragraph detection and be easier to grok.
          (Minus the parsing portion. That's not necessary.)

    Returns:
        A tuple of two values. The first is the block quote lines if a block quote was
        found, otherwise it is an empty list. The second value is the remaining text.
        (If lines does not start with a thematic break, it is the same as lines.)
    """
    block_quote: List[str] = []
    remaining_lines = lines

    while remaining_lines:
        if not is_explicit_block_quote_line(remaining_lines[0]):
            break

        while remaining_lines and is_explicit_block_quote_line(remaining_lines[0]):
            block_quote += [remaining_lines[0]]
            remaining_lines = remaining_lines[1:]

        check_for_continuation = _block_quote_ends_with_paragraph(block_quote)

        if check_for_continuation:
            first_line = True
            while remaining_lines and _is_paragraph_continuation_text(
                remaining_lines, line_offset
            ):
                if first_line:
                    first_line = False
                    if is_setext_underline(
                        remaining_lines[0]
                    ) and not is_thematic_break_line(remaining_lines[0]):
                        break
                block_quote += [remaining_lines[0]]
                remaining_lines = remaining_lines[1:]
                line_offset += 1
        else:
            break

    return block_quote, remaining_lines
