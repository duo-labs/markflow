from typing import List, Tuple

from ._lines import (
    is_blank_line_line,
    is_bullet_list_start_line,
    is_table_start_line,
    is_thematic_break_line,
)


def split_bullet_list(
    lines: List[str], line_offset: int = 0
) -> Tuple[List[str], List[str]]:
    bullet_list: List[str] = []
    remaining_lines = lines
    indexed_line_generator = enumerate(lines)

    index, line = next(indexed_line_generator)
    if not is_bullet_list_start_line(line):
        return bullet_list, remaining_lines

    bullet_list.append(line)
    for index, line in indexed_line_generator:
        if (
            is_blank_line_line(line)
            or is_table_start_line(line)
            or is_thematic_break_line(line)
        ):
            break
        else:
            bullet_list.append(line)
    else:
        # We consumed the last line, so increment our index to chop it off
        index += 1

    remaining_lines = remaining_lines[index:]
    return bullet_list, remaining_lines
