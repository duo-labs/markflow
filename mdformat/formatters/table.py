import enum
import math
import re

from ..typing import Number

from .base import MarkdownSection
from ..exceptions import MarkdownFormatException

__all__ = ["MarkdownTable"]

COLUMN_DIVIDER_REGEX = re.compile(r"(?<!\\)" r"\|")  # Ignore escaped |


class Alignment(enum.Enum):
    NONE = "none"
    CENTER = "center"
    LEFT = "left"
    RIGHT = "right"


def center_align(text: str, width: int) -> str:
    padding = width - len(text)
    leading_padding = math.floor(padding / 2)
    trailing_padding = math.ceil(padding / 2)
    return f"{' ' * leading_padding}{text}{' ' * trailing_padding}"


def left_align(text: str, width: int) -> str:
    padding = width - len(text)
    return f"{text}{' ' * padding}"


def right_align(text: str, width: int) -> str:
    padding = width - len(text)
    return f"{' ' * padding}{text}"


class MarkdownTable(MarkdownSection):
    def append(self, line: str) -> None:
        self.lines.append(line)

    def reformatted(self, width: Number = 88) -> str:
        column_widths = []
        for i, line in enumerate(self.lines):
            if i == 1:
                # Skip the divider line
                continue
            cols = COLUMN_DIVIDER_REGEX.split(line)[1:-1]
            cols = [col.strip() for col in cols]
            column_widths.append(tuple(len(col) for col in cols))

        column_alignments = []
        for divider in self.lines[1].strip()[1:-1].split("|"):
            divider = divider.strip()
            if divider.startswith(":") and divider.endswith(":"):
                column_alignments.append(Alignment.CENTER)
            elif divider.startswith(":"):
                column_alignments.append(Alignment.LEFT)
            elif divider.endswith(":"):
                column_alignments.append(Alignment.RIGHT)
            else:
                column_alignments.append(Alignment.NONE)

        header_column_count = len(column_widths[0])
        for i, column_width in enumerate(column_widths[1:], start=2):
            if len(column_width) != header_column_count:
                raise MarkdownFormatException(
                    f"Line {self.line_index + i + 1} has unexpected number of columns "
                    f"(expected: {header_column_count}, actual: {len(column_width)})"
                )

        new_column_widths = [0 for _ in column_widths[0]]
        for widths in column_widths:
            for i, width in enumerate(widths):
                if width > new_column_widths[i]:
                    new_column_widths[i] = width

        new_lines = []
        # First line is headers. We'll center them.
        headers = COLUMN_DIVIDER_REGEX.split(self.lines[0])[1:-1]
        header_strings = []
        for header, width, alignment in zip(
            headers, new_column_widths, column_alignments
        ):
            header = header.strip()
            if alignment == Alignment.CENTER:
                header_strings.append(f" {center_align(header, width)} ")
            elif alignment == Alignment.LEFT:
                header_strings.append(f" {left_align(header, width)} ")
            elif alignment == Alignment.RIGHT:
                header_strings.append(f" {right_align(header, width)} ")
            else:
                header_strings.append(f" {center_align(header, width)} ")
        new_lines.append("|" + "|".join(header_strings) + "|")

        # Second line is the dividers.
        dashes = []
        for width, alignment in zip(new_column_widths, column_alignments):
            divider = "-" * width
            if alignment == Alignment.CENTER:
                dashes.append(f":{divider}:")
            elif alignment == Alignment.LEFT:
                dashes.append(f":{divider}-")
            elif alignment == Alignment.RIGHT:
                dashes.append(f"-{divider}:")
            else:
                dashes.append(f"-{divider}-")
        new_lines.append(f"|{'|'.join(dashes)}|")

        # The rest are individual entries.
        for line in self.lines[2:]:
            columns = []
            for column, width, alignment in zip(
                line.split("|")[1:-1], new_column_widths, column_alignments
            ):
                column = column.strip()
                if alignment == Alignment.CENTER:
                    columns.append(f" {center_align(column, width)} ")
                elif alignment == Alignment.LEFT:
                    columns.append(f" {left_align(column, width)} ")
                elif alignment == Alignment.RIGHT:
                    columns.append(f" {right_align(column, width)} ")
                else:
                    columns.append(f" {left_align(column, width)} ")
            new_lines.append(f"|{'|'.join(columns)}|")

        return "\n".join(new_lines)
