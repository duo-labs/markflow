import abc

from typing import List
from ..typing import Number

__all__ = ["MarkdownSection"]


class MarkdownSection:
    def __init__(self, line_index: int):
        self.line_index = line_index
        self.lines: List[str] = []

    @abc.abstractmethod
    def append(self, line: str) -> None:
        """Append a line to this section"""

    @abc.abstractmethod
    def reformatted(self, width: Number = 88) -> str:
        """Reformat the section based on publicized rules"""
