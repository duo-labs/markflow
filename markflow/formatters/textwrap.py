import re

from typing import List, Tuple
from ..typing import Number

INLINE_CODE_MARKER_REGEX = re.compile(r"(((?!<\\)`)+)")
FOOTNOTE_REGEX = re.compile(r"\[[^\[]+\]\[[^\]]+\]")
HTML_NEWLINE_REGEX = re.compile(r"<br ?/?>")
URL_REGEX = re.compile(r"\[[^\[]+\]\([^\)]+\)")


def join(split_text: List[str], leading_spaces: List[bool], width: Number) -> str:
    new_split_text = [""]
    for word, leading_space in zip(split_text, leading_spaces):
        if leading_space and new_split_text[-1]:
            potential_new_string = f"{new_split_text[-1]} {word}"
        else:
            potential_new_string = f"{new_split_text[-1]}{word}"
        if len(potential_new_string) <= width or not new_split_text[-1]:
            new_split_text[-1] = potential_new_string
        else:
            new_split_text.append(word)

        # If we hit an HTML new line, the next text should begin on a new line.
        if HTML_NEWLINE_REGEX.match(word):
            new_split_text.append("")

    if not new_split_text[-1]:
        new_split_text = new_split_text[:-1]
    return "\n".join(new_split_text)


def code_split(
    text: str, leading_space: bool
) -> Tuple[List[str], List[bool], List[bool]]:
    split_text: List[str] = []
    leading_spaces: List[bool] = []
    evaluates: List[bool] = []

    # Markdown inline code only ends when the exact same number of tildas are seen
    # again. More or less indicates it is still part of the code.
    open_marker_len = 0
    last_end = 0
    # We jump from tilda mark to tilda mark. The length of the tildas indicate if we are
    # beginning, ending, or still in code.
    for code_marker in INLINE_CODE_MARKER_REGEX.finditer(text):
        if open_marker_len == 0:
            plaintext = text[last_end : code_marker.start()]  # noqa: E203
            if (
                plaintext.startswith(".")
                and not plaintext.startswith("..")
                and split_text
            ):
                split_text[-1] += "."
                plaintext = plaintext[1:]
            if plaintext.strip():
                if not leading_spaces:
                    leading_spaces.append(leading_space)
                else:
                    leading_spaces.append(plaintext.startswith(" "))
                split_text.append(plaintext.strip())
                evaluates.append(True)
            open_marker_len = len(code_marker.group())

            # Prepare our lists for code
            if not leading_spaces:
                leading_spaces.append(leading_space)
            else:
                leading_spaces.append(plaintext.endswith(" "))
            evaluates.append(False)
            split_text.append("`" * open_marker_len)
        elif len(code_marker.group()) == open_marker_len:
            # We've found the close of our inline code
            code = text[last_end : code_marker.start()]  # noqa: E203
            split_text[-1] += code + "`" * open_marker_len
            open_marker_len = 0
        else:
            # We've found more inline code
            split_text[-1] += text[last_end : code_marker.end()]  # noqa: E203

        last_end = code_marker.end()

    # If our last field only has a singular inline code marker, it means that it isn't
    # inline text and just a standalone tilda or set of tildas, so we can evaluate it.
    if split_text and len(INLINE_CODE_MARKER_REGEX.findall(split_text[-1])) == 1:
        evaluates[-1] = True
        if text[last_end:].strip():
            split_text[-1] += text[last_end:].rstrip()
    else:
        remaining_text = text[last_end:]
        if (
            remaining_text
            and remaining_text.startswith(".")
            and not remaining_text.startswith("..")
        ):
            split_text[-1] += "."
            remaining_text = remaining_text[1:]
        if remaining_text.strip():
            split_text.append(remaining_text.strip())
            if last_end == 0:
                leading_spaces.append(leading_space)
            else:
                leading_spaces.append(remaining_text.startswith(" "))
            evaluates.append(True)

    return split_text, leading_spaces, evaluates


def link_split(
    text: str, leading_space: bool
) -> Tuple[List[str], List[bool], List[bool]]:
    """ Splits text based on links

    This function iterates over text split by tildas. Markdown inline code begins with
    a number of tildas and only ends when that exact number is reached. If there are
    more tildas, e.g. `` ```` ``, they are treated as part of the inline code.

    Per our rules, inline code should all be on one line, so each inline code section is
    marked for non-evaluation.

    Args:
        text: The text to evaluate
        leading_space: Should this code section have a leading new space when reflowed?

    Returns:
        Split text, What sections have leading spaces, What sections should continue to
        be evaluated
    """
    matches = [m for m in FOOTNOTE_REGEX.finditer(text)]
    matches += [m for m in URL_REGEX.finditer(text)]
    matches.sort(key=lambda m: m.start())

    split_text: List[str] = []
    leading_spaces: List[bool] = []
    evaluates: List[bool] = []
    last_end = 0
    # Each iteration of this for loop operates operates on non-link text followed by
    # link text.
    for match in matches:
        non_link_text = text[last_end : match.start()]  # noqa: E203
        if non_link_text.strip():
            if (
                split_text
                and non_link_text.startswith(".")
                and not non_link_text.startswith("..")
            ):
                split_text[-1] += "."
                non_link_text = non_link_text[1:]
            split_text.append(non_link_text.strip())
            if not leading_spaces:
                leading_spaces.append(leading_space)
            else:
                leading_spaces.append(non_link_text.startswith(" "))

            leading_spaces.append(text[match.start() - 1] == " ")
            evaluates.append(True)
        else:
            if not leading_spaces:
                leading_spaces.append(leading_space)
            else:
                leading_spaces.append(False)

        leading_spaces.append(False)
        if "](" in match.group():
            split_link = match.group().split("](")
            split_text.append(split_link[0].strip() + "](")
            split_text.append(split_link[1].strip())
        else:
            split_link = match.group().split("][")
            split_text.append(split_link[0].strip() + "][")
            split_text.append(split_link[1].strip())

        # Don't modify our hyperlink
        evaluates += [True, False]
        last_end = match.end()

    remaining_text = text[last_end:]
    if (
        remaining_text
        and remaining_text.startswith(".")
        and not remaining_text.startswith("..")
    ):
        split_text[-1] += "."
        remaining_text = remaining_text[1:]
    if remaining_text.strip():
        split_text.append(remaining_text.strip())
        if last_end == 0:
            leading_spaces.append(leading_space)
        else:
            leading_spaces.append(remaining_text.startswith(" "))
        evaluates.append(True)

    return split_text, leading_spaces, evaluates


def newline_split(
    text: str, leading_space: bool
) -> Tuple[List[str], List[bool], List[bool]]:
    split_text: List[str] = []
    leading_spaces: List[bool] = []
    evaluates: List[bool] = []
    last_end = 0
    # Each iteration of this for loop operates operates on plaintext followed by an HML
    # newline.
    for match in HTML_NEWLINE_REGEX.finditer(text):
        non_newline_text = text[last_end : match.start()]  # noqa: E203
        if not leading_spaces:
            leading_spaces.append(leading_space)
        else:
            leading_spaces.append(text[last_end] == " ")

        if non_newline_text.strip():
            split_text.append(non_newline_text.strip())
            evaluates.append(True)
            leading_spaces.append(non_newline_text.endswith(" "))

        split_text.append(match.group())
        evaluates.append(False)
        last_end = match.end()

    if text[last_end:].strip():
        split_text.append(text[last_end:].strip())
        if last_end == 0:
            leading_spaces.append(leading_space)
        else:
            leading_spaces.append(text[last_end:].startswith(" "))
        evaluates.append(True)

    return split_text, leading_spaces, evaluates


def space_split(
    text: str, leading_space: bool
) -> Tuple[List[str], List[bool], List[bool]]:
    split_text: List[str] = []
    leading_spaces: List[bool] = []
    evaluates: List[bool] = []
    for word in text.split(" "):
        if not word:
            continue
        split_text.append(word.strip())
        if not leading_spaces:
            leading_spaces.append(leading_space)
        else:
            leading_spaces.append(True)
        evaluates.append(True)

    return split_text, leading_spaces, evaluates


def wrap(text: str, width: Number) -> str:
    lines = text.splitlines()
    text = " ".join([line.strip() for line in lines])

    split_text: List[str] = [text]
    leading_spaces: List[bool] = [False]
    evaluates: List[bool] = [True]
    for func in [code_split, link_split, newline_split, space_split]:
        new_split_text = []
        new_leading_spaces = []
        new_evaluates = []
        for text, leading_space, evaluate in zip(split_text, leading_spaces, evaluates):
            if evaluate:
                nst, nls, evl = func(text, leading_space)
                new_split_text += nst
                new_leading_spaces += nls
                new_evaluates += evl
            else:
                new_split_text.append(text)
                new_leading_spaces.append(leading_space)
                new_evaluates.append(evaluate)
        split_text = new_split_text
        leading_spaces = new_leading_spaces
        evaluates = new_evaluates

    return join(split_text, leading_spaces, width)
