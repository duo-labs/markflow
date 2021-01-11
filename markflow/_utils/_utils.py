__all__ = ["truncate_str"]

ELLIPSIS = "..."


def truncate_str(str_: str, length: int) -> str:
    if len(str_) <= length:
        pass
    elif len(ELLIPSIS) >= length:
        str_ = "." * length
    else:
        truncation = max(0, length - len(ELLIPSIS))
        str_ = str_[:truncation] + ELLIPSIS
    return str_
