from typing import IO, Any, AnyStr, Callable, Dict, Optional, Text, Union

from rich.highlighter import ReprHighlighter
from rich.style import Style
from typing_extensions import Literal

HighlighterType = Callable[[Union[str, Text]], Text]
JustifyValues = Optional[Literal["left", "center", "right", "full"]]

class Console:
    def __init__(
        self,
        color_system: Optional[
            Literal["auto", "standard", "256", "truecolor", "windows"]
        ] = ...,
        styles: Optional[Dict[str, Style]] = ...,
        file: Optional[IO[AnyStr]] = ...,
        width: Optional[int] = ...,
        height: Optional[int] = ...,
        record: bool = ...,
        markup: bool = ...,
        log_time: bool = ...,
        log_path: bool = ...,
        log_time_format: str = ...,
        highlighter: Optional[HighlighterType] = ...,
    ): ...
    def print(
        self,
        *objects: Any,
        sep: str = ...,
        end: str = ...,
        style: Optional[Union[str, Style]] = ...,
        emoji: bool = ...,
        highlight: bool = ...,
    ) -> None: ...
