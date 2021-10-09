from typing import Generator, List, Tuple

from ._lines import is_paragraph_start_line, is_setext_underline
from .atx_heading import split_atx_heading
from .blank_line import split_blank_line
from .block_quote import split_block_quote
from .bullet_list import split_bullet_list
from .fenced_code_block import split_fenced_code_block
from .ordered_list import split_ordered_list
from .table import split_table
from .thematic_break import split_thematic_break


def _is_paragraph_continuation_text(lines: List[str], line_offset: int = 0) -> bool:
    """Indicates whether the first line of lines would continue a paragraph

    This ensures that any valid interrupting section of a paragraph could not result in
    a valid block instead.

    We have a separate definition from the one used in block quote detection to avoid
    circular imports. That one also gets to skip block quote checking.

    Args:
        lines: The lines to evaluate.
        line_offset (optional): The offset into the overall document we are at. This is
            used for reporting errors in the original document.

    Returns:
        True if the first line would continue the paragraph. False otherwise.
    """
    for splitter in [
        split_atx_heading,
        split_blank_line,
        split_block_quote,
        split_bullet_list,
        split_fenced_code_block,
        split_ordered_list,
        split_table,
        split_thematic_break,
    ]:
        # ToDo: Disable logging?
        if splitter(lines, line_offset)[0]:
            return False
    if is_setext_underline(lines[0]):
        return False
    return True


def list_tail_generator(lines: List[str]) -> Generator[List[str], None, None]:
    """Generator that returns less and less of the end of a list

    The first call to this generator returns the passed in list. Each successive call
    to this generator returns the previous call without the first element until we
    return the last element.

    Args:
        lines: The lines to evaluate
        line_offset (optional): The offset into the overall document we are at. This is
            used for reporting errors in the original document.

    Returns:
        A tuple of two values. The first is the setext heading lines if they were found,
        otherwise it is an empty list. The second value is the remaining text. (If lines
        does not start with a thematic break, it is the same as lines.)

        The returned text can then be evaluated to determine if this is actually a
        paragraph or an setext heading.
    """
    for i in range(len(lines)):
        yield lines[i:]


def split_paragraph_ignoring_setext(
    lines: List[str], line_offset: int = 0
) -> Tuple[List[str], List[str]]:
    """Split a paragraph from beginning of lines if one exists

    Unlike split_paragraph, this does not take into account setext underlining. This is
    so that both detectors can share a common function.

    Args:
        lines: The lines to evaluate.
        line_offset (optional): The offset into the overall document we are at. This is
            used for reporting errors in the original document.

    Returns:
        A tuple of two values. The first is the paragraph lines if a paragraph was
        found, otherwise it is an empty list. The second value is the remaining text.
        (If lines does not start with a thematic break, it is the same as lines.)
    """
    paragraph_lines = []
    remaining_lines = lines

    if is_paragraph_start_line(lines[0]):
        # ToDo: This should be handled in `wrap` as a double space is always a newline
        #  in any section type. Also add indents while you're there.
        if lines[0].endswith("  "):
            return [lines[0]], lines[1:]
        paragraph_lines.append(lines[0])
        tail_lines_generator = list_tail_generator(lines[1:])
        for tail in tail_lines_generator:
            if _is_paragraph_continuation_text(
                tail, line_offset + len(paragraph_lines)
            ):
                paragraph_lines.append(tail[0])
                # ToDo: This should be handled in `wrap` as a double space is always a
                #  newline in any section type.
                if tail[0].endswith("  "):
                    remaining_lines = next(tail_lines_generator)
                    break
            else:
                remaining_lines = tail
                break
        else:
            remaining_lines = []

    return paragraph_lines, remaining_lines


def split_paragraph(
    lines: List[str], line_offset: int = 0
) -> Tuple[List[str], List[str]]:
    """Split a paragraph from beginning of lines if one exists

    Args:
        lines: The lines to evaluate.
        line_offset (optional): The offset into the overall document we are at. This is
            used for reporting errors in the original document.

    Returns:
        A tuple of two values. The first is the paragraph lines if a paragraph was
        found, otherwise it is an empty list. The second value is the remaining text.
        (If lines does not start with a thematic break, it is the same as lines.)
    """
    potential_paragraph, remaining_lines = split_paragraph_ignoring_setext(
        lines, line_offset
    )
    if not remaining_lines or not is_setext_underline(remaining_lines[0]):
        return potential_paragraph, remaining_lines
    else:
        return [], lines
