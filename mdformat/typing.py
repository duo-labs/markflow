from typing import Callable, List, Union

Number = Union[int, float]
SectionEndedFunc = Callable[[str, int, List[str]], bool]
