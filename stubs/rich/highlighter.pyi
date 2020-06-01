from typing import Union, Text

class Highlighter:
    def __call__(self, text: Union[str, Text]) -> Text: ...
    def highlight(self, text: Text) -> None: ...

# It doesn't derive from Highlighter directly, but that doesn't matter to us.
class ReprHighlighter(Highlighter): ...
