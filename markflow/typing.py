from typing import Callable, List, Tuple, Union

try:
    from typing import Protocol
except ImportError:
    # Python <3.8
    from typing_extensions import Protocol  # type: ignore

Number = Union[int, float]
SectionEndedFunc = Callable[[str, int, List[str]], bool]


class SplitFunc(Protocol):
    def __call__(
        self, lines: List[str], line_offset: int = 0
    ) -> Tuple[List[str], List[str]]:
        pass
