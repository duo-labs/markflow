from typing import Any, Callable, Iterable, List, Optional, Union

ExceptionClass = type

class MarkGenerator:
    def __getattr__(self, name: str) -> Any: ...
    @staticmethod
    def parametrize(
        argnames: str,
        argvalues: Union[List[Any], List[Iterable[Any]]],
        indirect: bool = ...,
        ids: Optional[Union[List[str], Callable[[Any], Optional[str]]]] = ...,
        scope: Optional[str] = ...,
    ) -> Callable[..., Any]: ...
    def xfail(
        self,
        condition: Optional[bool] = ...,
        reason: Optional[str] = ...,
        raises: Optional[ExceptionClass] = ...,
        run: bool = ...,
        strict: bool = ...,
    ) -> Callable[..., Any]: ...

def xfail(reason: str = ...) -> None: ...

mark: MarkGenerator
