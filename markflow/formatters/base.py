import abc
from typing import List, Optional

from ..typing import Number

__all__ = ["MarkdownSection"]


class MarkdownSection:
    def __init__(self, line_index: int, lines: Optional[List[str]] = None):
        self.line_index = line_index
        if lines is None:
            lines = []
        self.lines: List[str] = lines

    @abc.abstractmethod
    def reformatted(self, width: Number = 88) -> str:
        """Reformat the section based on publicized rules"""

    def __repr__(self) -> str:
        raise NotImplementedError("MarkdownSections must implement `__repr__`.")
