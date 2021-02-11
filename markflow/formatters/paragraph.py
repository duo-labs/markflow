from .._utils import truncate_str
from .._utils.textwrap import wrap
from ..typing import Number
from .base import MarkdownSection

__all__ = ["MarkdownParagraph"]

REPR_CONTENT_LEN = 20


class MarkdownParagraph(MarkdownSection):
    @property
    def content(self) -> str:
        # TODO: I think we actually want to split each line to remove double spaces.
        return " ".join([line.strip() for line in self.lines])

    def append(self, line: str) -> None:
        self.lines.append(line)

    def reformatted(self, width: Number = 88) -> str:
        text = wrap(self.content, width)
        if self.lines[-1].endswith("  "):
            text += "  "
        return text

    def __repr__(self) -> str:
        return (
            f"<"
            f"{self.__class__.__name__}: "
            f"content={repr(truncate_str(self.content, REPR_CONTENT_LEN))}"
            f">"
        )
