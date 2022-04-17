"""
MarkFlow Line Detection Library

This library is used a common space to evaluate position independent information about
lines. They are stored here so as to avoid any circular imports.
"""

import re

from .._utils import get_indent

FENCED_CODE_BLOCK_FENCE_CHARACTERS = ["`", "~"]
BULLET_LIST_START_REGEX = re.compile(
    r"^\s*"  # Leading spaces are OK and often expected
    r"["
    r"*"  # Asterisk list marker
    r"+"  # Plus list marker
    r"-"  # Dash list marker
    r"] "  # Lists need a space after their identifier
)
ORDERED_LIST_START_REGEX = re.compile(
    r"^\s*"  # Leading spaces are OK and often expected
    r"("
    r"[0-9]+\."  # Numeric list marker
    r") "  # Lists need a space after their identifier
)
THEMATIC_BREAK_CHARACTERS = ["*", "_", "-"]


def is_atx_heading_line(line: str) -> bool:
    """Evaluates whether a line is formatted like an ATX heading

    The standard requires a space, but it also notes that not everyone follows this. We
    are lax in our definition and fix it on reformatting.

    Examples:
        ```
        #Heading
        # Heading
        ```

    Args:
        line: The line to evaluate

    Returns:
        True if the line is an ATX heading. False otherwise.
    """
    return not is_indented_code_block_start_line(line) and line.lstrip().startswith("#")


def is_blank_line_line(line: str) -> bool:
    """Evaluates whether a line is a blank line

    Example:
        ```

        ```

    Args:
        line: The line to evaluate

    Returns:
        True if the line is an ATX heading. False otherwise.
    """
    return not line.strip()


def is_explicit_block_quote_line(line: str) -> bool:
    """Evaluates whether a line is explicitly block quote line

    The distinction here is that paragraph continuation lines can be part of a block
    quote. This ensures that is what is desired.

    Example:
        ```
        > Block Quote
        ```

    Args:
        line: The line to evaluate

    Returns:
        True if the line is an block quote line. False otherwise.
    """
    return not is_indented_code_block_start_line(line) and line.lstrip().startswith(">")


def is_fenced_code_block_start_line(line: str) -> bool:
    """Evaluates whether a line could open a fenced code block

    Examples:
        ```
        ```python3
        ~~~markdown
        ```

    Args:
        line: The line to evaluate

    Returns:
        True if the line is could open a fenced code block. False otherwise.
    """
    for fence in FENCED_CODE_BLOCK_FENCE_CHARACTERS:
        if line.strip().startswith(fence * 3):
            return True
    return False


def is_indented_code_block_start_line(line: str) -> bool:
    """Evaluates whether a line could start and indented code block

    Examples:
        ```
            There's four spaces before this
        ```

    Args:
        line: The line to evaluate

    Returns:
        True if the line is could start an indented code block. False otherwise.
    """
    return bool(line.strip()) and get_indent(line) >= 4


def is_ordered_list_start_line(line: str) -> bool:
    """Evaluates whether a line could start an ordered list

    Example:
        ```
        1. Entry
        ```

    Args:
        line: The line to evaluate

    Returns:
        True if the line is could start an ordered list. False otherwise.
    """
    return not is_indented_code_block_start_line(line) and bool(
        ORDERED_LIST_START_REGEX.search(line)
    )


def is_bullet_list_start_line(line: str) -> bool:
    """Evaluates whether a line could start a bullet list

    Example:
        ```
        * Asterisk List
        - Dash List
        + Plus List
        ```

    Args:
        line: The line to evaluate

    Returns:
        True if the line is could start a bullet list. False otherwise.
    """
    return not is_indented_code_block_start_line(line) and bool(
        BULLET_LIST_START_REGEX.search(line)
    )


def is_paragraph_start_line(line: str) -> bool:
    """Evaluates whether a line could start a paragraph

    We basically evaluate that no other section type could start instead.

    Examples:
        ```
        Just some text
        ```

    Args:
        line: The line to evaluate

    Returns:
        True if the line is could start a list. False otherwise.
    """
    for line_checker in [
        is_indented_code_block_start_line,
        is_atx_heading_line,
        is_blank_line_line,
        is_bullet_list_start_line,
        is_explicit_block_quote_line,
        is_fenced_code_block_start_line,
        is_ordered_list_start_line,
        is_table_start_line,
        is_thematic_break_line,
    ]:
        if line_checker(line):
            return False
    return True


def is_setext_underline(line: str) -> bool:
    """Evaluates whether a line could be the underlining for a setext heading

    Examples:
        ```
        ---
          ==
        ```

    Args:
        line: The line to evaluate

    Returns:
        True if the line is could underline an setext heading. False otherwise.
    """
    return (
        not is_indented_code_block_start_line(line)
        and bool(line.strip())
        and (
            all([c == "=" for c in line.strip()])
            or all([c == "-" for c in line.strip()])
        )
    )


def is_table_start_line(line: str) -> bool:
    """Evaluates whether a line could start a table

    Examples:
        ```
        |Table|
        ```

    Args:
        line: The line to evaluate

    Returns:
        True if the line is could start a table. False otherwise.
    """
    # ToDo: Not really, but we'll have to adapt a standard from somewhere other than
    #  CommonMark
    return line.lstrip().startswith("|")


def is_thematic_break_line(line: str) -> bool:
    if is_indented_code_block_start_line(line):
        return False

    spaceless_line = "".join(line.split())
    if len(spaceless_line) < 3:
        # Thematic breaks must be at least three characters long
        return False
    else:
        for symbol in THEMATIC_BREAK_CHARACTERS:
            if all(char == symbol for char in spaceless_line.strip()):
                return True
        else:
            return False
