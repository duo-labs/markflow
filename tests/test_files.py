import logging
import os
import pathlib

from typing import DefaultDict, List, Optional

import pytest

from mdformat import reformat_markdown_text

from .util import render

logger = logging.getLogger(__name__)


# TODO: File bug report for 0015
PYCOMMONMARK_BUG_FILES = ["0015"]
MDFORMAT_BUG_FILES = ["0016", "0017", "0018"]


class FilePair:
    def __init__(self) -> None:
        self._input: Optional[pathlib.Path] = None
        self._output: Optional[pathlib.Path] = None

    @property
    def valid(self) -> bool:
        return bool(
            self._input
            and self._input.is_file()
            and self._output
            and self._output.is_file()
        )

    @property
    def input(self) -> pathlib.Path:
        if self._input is None:
            raise RuntimeError("Input file not defined.")
        return self._input

    @input.setter
    def input(self, path: pathlib.Path) -> None:
        self._input = path

    @property
    def output(self) -> pathlib.Path:
        if self._output is None:
            raise RuntimeError("Input file not defined.")
        return self._output

    @output.setter
    def output(self, path: pathlib.Path) -> None:
        self._output = path

    def __str__(self) -> str:
        return f"<{self.__class__.__name__}: {self.input} -> {self.output}>"

    def __repr__(self) -> str:
        return str(self)


def get_file_pairs(directory: pathlib.Path) -> List[FilePair]:
    file_pairs = DefaultDict[str, FilePair](FilePair)
    for file in directory.iterdir():
        if file.is_dir():
            continue
        key, arg, _ = file.name.split("_", maxsplit=2)
        if arg.startswith("in"):
            file_pairs[key].input = file
        elif arg.startswith("out"):
            file_pairs[key].output = file
    for pair in file_pairs.values():
        assert pair.valid, f"{pair} is not a valid pair of files"

    return sorted(list(file_pairs.values()), key=lambda f: f.input)


class TestFiles:
    @pytest.mark.parametrize(
        "file_pair",
        get_file_pairs(
            pathlib.Path(os.path.dirname(os.path.realpath(__file__))).resolve()
            / "files"
        ),
    )
    def test_files(self, file_pair: FilePair) -> None:
        if any(num in file_pair.input.name for num in MDFORMAT_BUG_FILES):
            pytest.xfail("Marking test xfail due to mdformat bug.")

        input_text = file_pair.input.read_text()
        output_text = file_pair.output.read_text()
        reformatted = reformat_markdown_text(input_text)
        assert reformatted == output_text
        rereformatted = reformat_markdown_text(reformatted)
        assert rereformatted == output_text
        if "|--" in input_text:
            logger.info(
                "Skipping render check as there are tables are not supported by the "
                "commonmark Python library."
            )
        elif any(num in file_pair.input.name for num in PYCOMMONMARK_BUG_FILES):
            logger.info(
                "Skipping render check due to a bug in the commonmark Python library."
            )
        else:
            assert render(output_text) == render(input_text)
