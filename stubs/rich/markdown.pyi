from typing import Union

from rich.console import JustifyValues
from rich.style import Style

class Markdown:
    def __init__(
        self,
        markup: str,
        code_theme: str = ...,
        justify: JustifyValues = ...,
        style: Union[str, Style] = ...,
    ) -> None: ...
