"""
MarkFlow Fenced Code Block Detection Library

Fenced code blocks are multiple lines of text that open with a line beginning with at
least two asterisks or tildas that ends with that same sequence on its own line.

Examples:
    ```
    ``
    print("Hello world!")
    ``
    ```

    ```
    ~~~~
    print("Hello world!")
    ~~~~
    ```
"""

"""
4.5 Fenced code blocks

A code fence is a sequence of at least three consecutive backtick characters (`) or
tildes (~). (Tildes and backticks cannot be mixed.) A fenced code block begins with a
code fence, indented no more than three spaces.

The line with the opening code fence may optionally contain some text following the
code fence; this is trimmed of leading and trailing whitespace and called the info
string. If the info string comes after a backtick fence, it may not contain any backtick
characters. (The reason for this restriction is that otherwise some inline code would
be incorrectly interpreted as the beginning of a fenced code block.)

The content of the code block consists of all subsequent lines, until a closing code
fence of the same type as the code block began with (backticks or tildes), and with at
least as many backticks or tildes as the opening code fence. If the leading code fence
is indented N spaces, then up to N spaces of indentation are removed from each line of
the content (if present). (If a content line is not indented, it is preserved unchanged.
If it is indented less than N spaces, all of the indentation is removed.)

The closing code fence may be indented up to three spaces, and may be followed only by
spaces, which are ignored. If the end of the containing block (or document) is reached
and no closing code fence has been found, the code block contains all of the lines after
the opening code fence until the end of the containing block (or document). (An
alternative spec would require backtracking in the event that a closing code fence is
not found. But this makes parsing much less efficient, and there seems to be no real
down side to the behavior described here.)

A fenced code block may interrupt a paragraph, and does not require a blank line either
before or after.

https://spec.commonmark.org/0.29/#fenced-code-blocks
"""

import logging

from typing import List, Tuple

from .._utils import get_indent

logger = logging.getLogger(__name__)

# TODO: This is really dirty; let's probably make started functions return ended
#  functions; I'm not doing that yet in case a better pattern emerges on the rest of
#  this refactor
# The alternative is every time fenced_code_block_ended is called, we walk backwards to
# find the fence.

FENCES = "`~"
__LAST_FENCE = ""
__LAST_FENCE_INDEX = -1


def fenced_code_block_started(line: str, index: int, lines: List[str]) -> bool:
    """DEPRECATED"""
    global __LAST_FENCE
    global __LAST_FENCE_INDEX
    for fence in FENCES:
        if line.strip().startswith(fence * 3):
            count = len(line.strip()) - len(line.strip().lstrip(fence))
            __LAST_FENCE = fence * count
            __LAST_FENCE_INDEX = index
            return True
    return False


def fenced_code_block_ended(line: str, index: int, lines: List[str]) -> bool:
    """DEPRECATED"""
    # We'll catch even over indented fences assuming that that was an accident.
    global __LAST_FENCE
    global __LAST_FENCE_INDEX
    if not __LAST_FENCE:
        raise RuntimeError("End of fenced code block attempted without starting one.")

    # If we're on the last line, we'll still want to warn about the fence indentation
    if index + 1 == len(lines):
        # TODO: We add the last fence because this is used for parsing lists, and we
        #  allow indented code blocks in lists. But, those are actually inline code
        #  blocks according to the example render.
        last_fence_indent = len(lines[__LAST_FENCE_INDEX]) - len(
            lines[__LAST_FENCE_INDEX].lstrip()
        )
        if (
            line.strip().startswith(__LAST_FENCE)
            and len(line) - len(line.lstrip()) > 3 + last_fence_indent
        ):
            logger.warning(
                "Detected that the fence on line %d is over indented per the standard. "
                "If this is intentional, please file a bug report." % (index + 1)
            )

    # We'll just redetect our opening line
    if index - 1 == __LAST_FENCE_INDEX:
        return False

    last_line = lines[index - 1]
    if last_line.strip().startswith(__LAST_FENCE):
        last_fence_indent = len(lines[__LAST_FENCE_INDEX]) - len(
            lines[__LAST_FENCE_INDEX].lstrip()
        )
        if len(last_line) - len(last_line.lstrip()) > 3 + last_fence_indent:
            logger.warning(
                "Detected that the fence on line %d is over indented per the standard. "
                "If this is intentional, please file a bug report." % (index + 1)
            )
        __LAST_FENCE = ""
        __LAST_FENCE_INDEX = -1
        return True
    return False


def split_fenced_code_block(
    lines: List[str], line_offset: int = 0
) -> Tuple[List[str], List[str]]:
    """Split leading fenced code block from lines if one exists

    Args:
        lines: The lines to evaluate.
        line_offset (optional): The offset into the overall document we are at. This is
            used for reporting errors in the original document.

    Returns:
        A tuple of two values. The first is the fenced code block lines if they were
        found, otherwise it is `None`. The second value is the remaining text. (If lines
        does not start with a fenced code block, it is the same as lines.)
    """
    # TODO: Fenced code blocks can't be indented
    fenced_code_block: List[str] = []
    remaining_lines = lines
    indexed_line_generator = enumerate(lines)

    index, line = next(indexed_line_generator)
    for fence in FENCES:
        if line.strip().startswith(fence * 3):
            count = len(line.lstrip()) - len(line.lstrip().lstrip(fence))
            fence_indent = get_indent(line)
            full_fence = fence * count
            break
    else:
        return fenced_code_block, remaining_lines

    fenced_code_block.append(line)

    for index, line in indexed_line_generator:
        fenced_code_block.append(line)
        if line.strip() == full_fence:
            if get_indent(line) > 3 + fence_indent:
                logger.warning(
                    "Detected that the fence on line %d is over indented per the "
                    "standard. If this is intentional, please file a bug report."
                    % (index + line_offset + 1)
                )
            break

    remaining_lines = remaining_lines[index + 1 :]
    return fenced_code_block, remaining_lines
