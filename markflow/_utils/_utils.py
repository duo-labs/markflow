__all__ = ["line_is_indented_at_least", "line_is_indented_less_than", "truncate_str"]

ELLIPSIS = "..."


def line_is_indented_less_than(line: str, count: int) -> bool:
    return len(line) - len(line.lstrip()) < count


def line_is_indented_at_least(line: str, count: int) -> bool:
    return not line_is_indented_less_than(line, count)


def truncate_str(str_: str, length: int) -> str:
    if len(str_) <= length:
        pass
    elif len(ELLIPSIS) >= length:
        str_ = "." * length
    else:
        truncation = max(0, length - len(ELLIPSIS))
        str_ = str_[:truncation] + ELLIPSIS
    return str_
