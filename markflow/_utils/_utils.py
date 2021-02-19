import contextlib
import logging
from typing import Iterator

__all__ = [
    "get_indent",
    "truncate_str",
    "redirect_info_logs_to_debug",
]

ELLIPSIS = "..."


def get_indent(line: str) -> int:
    return len(line) - len(line.lstrip())


def truncate_str(str_: str, length: int) -> str:
    if len(str_) <= length:
        pass
    elif len(ELLIPSIS) >= length:
        str_ = "." * length
    else:
        truncation = max(0, length - len(ELLIPSIS))
        str_ = str_[:truncation] + ELLIPSIS
    return str_


@contextlib.contextmanager
def redirect_info_logs_to_debug() -> Iterator[None]:
    old_info = logging.INFO
    logging.INFO = logging.DEBUG
    yield
    logging.INFO = old_info
