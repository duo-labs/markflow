import argparse
import dataclasses
import glob
import os
import pathlib

from typing import cast, Any, Callable, List, Optional, Sequence, Union


@dataclasses.dataclass(frozen=True)
class Permission:
    os_constant: int
    verbiage: str


EXECUTABLE = Permission(os.X_OK, "execute")
READABLE = Permission(os.R_OK, "read from")
WRITABLE = Permission(os.W_OK, "write to")


class ExistingPath:
    def __init__(self, permissions: List[Permission]):
        self._permissions = permissions

    def __call__(self, string: str) -> pathlib.Path:
        path = pathlib.Path(string)
        if not path.exists():
            raise argparse.ArgumentTypeError(
                f"specified path does not exist: {repr(str(path))}"
            )
        return path


class Directory:
    def __init__(self, permissions: List[Permission], must_exist: bool = False):
        self._permissions = permissions
        self._must_exist = must_exist

    def __call__(self, string: str) -> pathlib.Path:
        path = pathlib.Path(string)
        if path.exists():
            if not path.is_dir():
                raise argparse.ArgumentTypeError(
                    f"specified directory is a file: {repr(str(path))}"
                )

            for permission in self._permissions:
                if not os.access(path, permission.os_constant):
                    raise argparse.ArgumentTypeError(
                        f"cannot {permission.verbiage} directory: " f"{repr(str(path))}"
                    )
        else:
            if self._must_exist:
                raise argparse.ArgumentTypeError(
                    f"directory does not exist: {repr(str(path))}"
                )
        return path


class File:
    def __init__(self, permissions: List[Permission], must_exist: bool = False):
        self._permissions = permissions
        self._must_exist = must_exist

    def __call__(self, string: str) -> pathlib.Path:
        path = pathlib.Path(string)
        if path.exists():
            if path.is_dir():
                raise argparse.ArgumentTypeError(
                    f"file is a directory: {repr(str(path))}"
                )

            for permission in self._permissions:
                if not os.access(path, permission.os_constant):
                    raise argparse.ArgumentTypeError(
                        f"can't {permission.verbiage} file: {repr(str(path))}"
                    )
        else:
            if self._must_exist:
                raise argparse.ArgumentTypeError(
                    f"file does not exist: {repr(str(path))}"
                )

            if not path.parent.is_dir():
                raise argparse.ArgumentTypeError(
                    f"directory does not exist for file: {repr(str(path))}"
                )

            for permission in self._permissions:
                if not os.access(path.parent, permission.os_constant):
                    raise argparse.ArgumentTypeError(
                        f"cannot {permission.verbiage} directory of file: "
                        f"{repr(str(path))}"
                    )
        return path


class AddMarkdownFilesInDirOrPathsAction(argparse.Action):
    def __init__(
        self,
        option_strings: List[str],
        dest: str,
        type: Callable[[str], pathlib.Path],
        nargs: Optional[str] = None,
        **kwargs: Any,
    ):
        if nargs != "*":
            raise ValueError("nargs must be *")
        super().__init__(option_strings, dest, type=type, nargs=nargs, **kwargs)

    def __call__(
        self,
        parser: argparse.ArgumentParser,
        namespace: argparse.Namespace,
        values: Union[str, Sequence[Any], None],
        option_string: Optional[str] = None,
    ) -> None:
        if values is None:
            return
        values = cast(Sequence[pathlib.Path], values)
        expanded_paths = []
        for value in values:
            if value.is_file():
                expanded_paths.append(value)
            else:
                markdown_paths = glob.glob(str(value / "*.md"))
                markdown_paths += glob.glob(str(value / "**" / "*.md"))
                expanded_paths += [pathlib.Path(path) for path in markdown_paths]
        setattr(namespace, self.dest, expanded_paths)
