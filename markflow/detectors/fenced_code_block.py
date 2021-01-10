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
"""

import logging

from typing import List

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
    # We'll catch even over indented fences assuming that that was an accident.
    global __LAST_FENCE
    global __LAST_FENCE_INDEX
    if not __LAST_FENCE:
        raise RuntimeError("End of fenced code block attempted without starting one.")
    # We'll just redetect our opening line
    if index - 1 == __LAST_FENCE_INDEX:
        return False

    last_line = lines[index - 1]
    if last_line.strip().startswith(__LAST_FENCE):
        if len(last_line) - len(last_line.lstrip()) > 3:
            logger.warning(
                "Detected that the fence on line %d is over indented per the standard. "
                "If this is intentional, please file a bug report." % (index + 1)
            )
        __LAST_FENCE = ""
        __LAST_FENCE_INDEX = -1
        return True
    return False
