import argparse
import logging
import math
import pathlib
import sys

from typing import List, TextIO
from .typing import Number

import rich.console
import rich.logging
import rich.markdown

from .exceptions import MarkdownFormatException, ReformatInconsistentException
from .reformat_markdown import reformat_markdown_text, _reformat_markdown_text
from ._argparse import (
    AddMarkdownFilesInDirOrPathsAction,
    Directory,
    ExistingPath,
    File,
    READABLE,
    WRITABLE,
)

logger = logging.getLogger(__name__)


def print_markdown(markdown_text: str) -> None:
    console = rich.console.Console()
    console.print(rich.markdown.Markdown(markdown_text))


def parse_args(argv: List[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Make your Markdown sparkle.", add_help=False
    )

    developer_options = [
        "--dev-help",
        "--developer-help",
        "--output-dir",
        "--output-directory",
        "--output-file",
        "--write-renders",
    ]
    show_developer_help = any(o in argv for o in developer_options)

    # Overwrite the default help in order to grammatically correct the help message.
    parser.add_argument(
        "-h",
        "--help",
        action="help",
        help="Show this help message and exit."
        if not show_developer_help
        else "Show the non-developer help message and exit.",
    )
    parser.add_argument(
        "--line-length",
        default=88,
        type=int,
        help=(
            "The desired maximum length of lines in your file. Pass any number less"
            "than 1 to set the line length to infinity. (default: %(default)s)"
        ),
    )
    parser.add_argument(
        "paths",
        action=AddMarkdownFilesInDirOrPathsAction,
        nargs="*",
        type=ExistingPath([READABLE]),
        help="Path(s) to file(s) to reformat.",
    )

    parser.add_argument(
        "--check",
        action="store_true",
        default=False,
        help="Don't update file, just check if it would be reformatted.",
    )

    parser.add_argument(
        "-v",
        "--verbose",
        action="count",
        default=0,
        help="Increase output verbosity. Pass multiple times to increase output "
        "further.",
    )
    parser.add_argument(
        "-q",
        "--quiet",
        default=0,
        action="count",
        help="Decrease output verbosity. Pass multiple times to reduce output further.",
    )

    dev_arguments = parser.add_argument_group("developer arguments")
    dev_arguments.add_argument(
        "--dev-help",
        "--developer-help",
        default=False,
        dest="developer_help",
        action="store_true",
        help="Show this help message and exit."
        if show_developer_help
        else argparse.SUPPRESS,
    )
    output_arguments = dev_arguments.add_mutually_exclusive_group(required=False)
    output_arguments.add_argument(
        "--output-dir",
        "--output-directory",
        dest="output_directory",
        type=Directory(permissions=[WRITABLE], must_exist=True),
        help=(
            "Write rendered Markdown files to a separate folder instead of overwriting "
            "the files in place. Useful for comparing inputs and outputs. You can "
            "only specify output files or an output directory."
        )
        if show_developer_help
        else argparse.SUPPRESS,
    )
    output_arguments.add_argument(
        "--output-file",
        dest="output_files",
        type=File(permissions=[WRITABLE], must_exist=False),
        action="append",
        help=(
            "Write the output of markflow to a file. You must specify as many output "
            "files as there are input files. The two lists of files will be "
            "co-indexed. You can only specify output files or an output directory."
        )
        if show_developer_help
        else argparse.SUPPRESS,
    )
    dev_arguments.add_argument(
        "--write-renders",
        action="store_true",
        help=(
            "Write each rendering step to a different file if the renderings are "
            "inconsistent. The file with the first formatting is named with a .1 (i.e. "
            "file.md -> file.1.md, file -> file.1) and the second with a .2. Note: "
            "This will result in the file being parsed four times: twice for first "
            "pass to detect the error, then twice more to generate the files."
        )
        if show_developer_help
        else argparse.SUPPRESS,
    )

    args = parser.parse_args(argv)

    logging_levels = [
        logging.DEBUG,
        logging.INFO,
        logging.WARNING,
        logging.ERROR,
        logging.CRITICAL,
    ]
    # Default logging level is ERROR
    verbosity = logging_levels.index(logging.ERROR) - args.verbose + args.quiet
    verbosity = max(0, min(verbosity, len(logging_levels) - 1))
    logging.basicConfig(
        format="",
        level=logging_levels[verbosity],
        handlers=[rich.logging.RichHandler()],
    )

    if args.developer_help:
        # Since the developer help option was passed, we haven't suppressed the help
        # output. Sadly, we can't just add another 'help' action, so we need to do this
        # by hand.
        parser.print_help()
        sys.exit(-1)

    # We need to ensure there are enough files to write to.
    if args.output_files and len(args.paths) != len(args.output_files):
        parser.print_usage()
        print(
            f"{parser.prog}: error: argument(s) --output-file: invalid number of "
            f"files specified: expected {len(args.paths)} passed "
            f"{len(args.output_files)}"
        )
        sys.exit(-1)

    # If we aren't writing to other files, ensure we can write to the files that were
    # passed in as we only guaranteed they were readable by `parse_args`. We sort of
    # duplicate argparse's parameter construction here to do so.
    if not args.output_files and not args.output_directory and not args.check:
        for path in args.paths:
            try:
                File([WRITABLE])(path)
            except argparse.ArgumentTypeError as ate:
                parser.print_usage()
                print(f"{parser.prog}: error: argument paths: {str(ate)}")
                sys.exit(-1)

    return args


def _write_renders(
    input_path: pathlib.Path, output_path: pathlib.Path, width: Number = 88
) -> None:
    if output_path.name.endswith(".md"):
        first_output_name = output_path.name[:-3] + ".1.md"
        second_output_name = output_path.name[:-3] + ".2.md"
    else:
        first_output_name = output_path.name + ".1"
        second_output_name = output_path.name + ".2"

    first_output_path = output_path.parent / first_output_name
    first_contents = _reformat_markdown_text(input_path.read_text(), width)
    logger.debug("Writing first render to %s", first_output_path)
    first_output_path.write_text(first_contents)

    second_output_path = output_path.parent / second_output_name
    logger.debug("Writing second render to %s", second_output_path)
    second_contents = _reformat_markdown_text(first_contents, width)
    second_output_path.write_text(second_contents)


def _print_renders(text: str, width: Number = 88) -> None:
    first_contents = _reformat_markdown_text(text, width)
    logger.debug("Writing first render to STDOUT")
    print(first_contents)

    second_contents = _reformat_markdown_text(first_contents, width)
    logger.debug("Writing second render to STDOUT")
    print(second_contents)


def _reformat_files(args: argparse.Namespace) -> int:
    if args.output_directory:
        output_paths = [args.output_directory / p.name for p in args.paths]
    elif args.output_files:
        output_paths = args.output_files
    else:
        output_paths = args.paths

    files_left_unchanged = 0
    files_changed = 0
    for input_path, output_path in zip(args.paths, output_paths):
        old_contents = input_path.read_text()
        try:
            new_contents = reformat_markdown_text(old_contents, args.line_length)
        except RuntimeError as runtime_error:
            if args.write_renders and isinstance(
                runtime_error, ReformatInconsistentException
            ):
                _write_renders(input_path, output_path, args.line_length)
            # Add file information to our exception
            new_args = []
            new_args.append(runtime_error.args[0] + f" (file: {str(input_path)})")
            for arg in runtime_error.args[1:]:
                new_args.append(arg)
            runtime_error.args = tuple(new_args)
            raise
        if new_contents != old_contents:
            files_changed += 1
            if not args.check:
                output_path.write_text(new_contents)
                print_markdown(f"**reformatted {input_path}**")
            else:
                print_markdown(f"would reformat {input_path}")
        else:
            if output_path != input_path:
                output_path.write_text(new_contents)
            files_left_unchanged += 1

    print_markdown("All done!")
    messages: List[str] = []
    return_value = 0
    if args.check:
        if files_changed:
            file_word = "file" if files_changed == 1 else "files"
            messages.append(f"**{files_changed} {file_word} would be reformatted.**")
            return_value = 1
        if files_left_unchanged:
            file_word = "file" if files_left_unchanged == 1 else "files"
            messages.append(
                f"{files_left_unchanged} {file_word} would be left unchanged."
            )
    else:
        if files_changed:
            file_word = "file" if files_changed == 1 else "files"
            file_verb = "was" if files_changed == 1 else "were"
            messages.append(f"**{files_changed} {file_word} {file_verb} reformatted.**")
        if files_left_unchanged:
            file_word = "file" if files_left_unchanged == 1 else "files"
            file_verb = "was" if files_left_unchanged == 1 else "were"
            messages.append(
                f"{files_left_unchanged} {file_word} {file_verb} left unchanged."
            )
    print_markdown(" ".join(messages))
    return return_value


def _reformat_stdin(args: argparse.Namespace, stdin: TextIO) -> int:
    if args.output_directory or args.output_files:
        logger.warning(
            "MarkFlow is being run in interactive mode. Results will be written to "
            "STDOUT."
        )

    old_contents = stdin.read()
    try:
        new_contents = reformat_markdown_text(old_contents, args.line_length)
    except RuntimeError as runtime_error:
        if args.write_renders and isinstance(
            runtime_error, ReformatInconsistentException
        ):
            _print_renders(old_contents, args.line_length)
        raise

    if args.check:
        if new_contents != old_contents:
            print_markdown(f"STDIN would be reformatted.")
            return 1
        else:
            print_markdown("STDIN would be unchanged.")
            return 0
    else:
        print(new_contents, end="")
        return 0


def main(argv: List[str]) -> int:
    args = parse_args(argv)

    if args.line_length < 1:
        args.line_length = math.inf

    if not args.paths:
        if sys.stdin.isatty():
            print_markdown("**No path provided. Nothing to do.**")
            return 0
        else:
            return _reformat_stdin(args, sys.stdin)
    else:
        return _reformat_files(args)


def __main__() -> None:
    try:
        exit(main(sys.argv[1:]))
    except MarkdownFormatException as md_exception:
        logger.error(md_exception)
        exit(-1)


if __name__ == "__main__":
    __main__()
