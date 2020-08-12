# MarkFlow

Welcome to MarkFlow. This tool automatically reformats your Markdown to provided
consistent looking Markdown files.

## Quickstart

To use this tool, install it with pip then run `markflow`:

```shell
pip install markflow
markflow SOMETHING.md
```

To install from source, assuming you already have `poetry` installed, from the project
directory, run:

```shell
poetry install
poetry run markflow
```

Just want to see if there will be any changes? Use the `--check` flag:

```shell
markflow --check $PATH_TO_MARKDOWN_FILE
```

## Enforced Rules

The tool ensures that the following rules are enforced for each different type of
Markdown section. For all sections, trailing spaces on each line are removed. It also
ensures that Markdown files end with a single newline and newlines are all `'\n'`.

This tools uses the Markdown standard defined by [CommonMark 0.29][commonmark]. It is
expected to evolve with the standard and this section will be updated as support is
added. If you notice an discrepancies, please open an issue.

[commonmark_spec]: https://spec.commonmark.org/0.29/

### Block Quotes

Block quotes are fixed up with proper indentation markers for indented quotes, quote
indicators have any space between them removed, and unescaped `>` that could be confused
with quote markers are escaped. e.g:

```markdown
>
> > Text >
> >
>
> > Ice Cream \> 0O0>
>
```

becomes:

```markdown
>
>> Text \>
>>
>
>> Ice Cream \>  0O0>
>
```

### Code Blocks

Code block marker lines begin and end with no whitespace.

### Footnotes

Footnote lines begin and end with no whitespace.

### Headings

Heading lines being and end with no whitespace. If you are using underlined headings,
they will automatically be fixed to ensure underlining matches the heading length. e.g:

```markdown
Heading 1
--
```

becomes

```markdown
Heading 1
---------
```

### Horizontal Lines

Horizontal Lines are extended or reduced to match the length of the document. If line
length is set to infinity, it will instead use 3 dashes.

### Lists

Lists will be corrected to proper indentation. In addition, ordered lists will be
properly numbered and bullet lists will be reformatted to use consistent bullets. Line
lengths are also enforces. e.g:

```markdown
1. One
    * Asterisk
  - Dash
1. Two
5. Three
```

becomes

```markdown
1. One
  * Asterisk
  * Dash
2. Two
3. Three
```

### Paragraphs

Paragraphs are reformatted to ensure they are the proper length. URLs and footnotes are
properly split across lines. Inline code is placed all on a singular line. e.g.
(assuming a line length of 1):

```markdown
test `test =
1` [url](http://example.com)
```

becomes:

```markdown
test
`test = 1`
[url](
http://example.com)
```

### Separators

Separating lines (i.e. blank lines) contain only new lines, removing any horizontal
whitespace.

### Tables

Tables are reformatted to ensure proper width and headings are centered and all cells
have at minimum one space between their contents and column separators. Alignment is
supported too! e.g:

```markdown
|L|C|R|N|
|:--|:-:|--:|---|
|a|a|a|a|
|aa|aa|aa|aa|
|abcde|abcde|abcde|abcde|
```

becomes:

```markdown
| L     |   C   |     R |   N   |
|:------|:-----:|------:|-------|
| a     |   a   |     a | a     |
| aa    |  aa   |    aa | aa    |
| abcde | abcde | abcde | abcde |
```

[commonmark_pkg]: https://github.com/readthedocs/commonmark.py

## API Reference

The tool also provides a function to reformat markdown strings yourself.

```python
from markflow import reformat_markdown_text

markdown = "   # Header 1"
nice_markdown = reformat_markdown_text(markdown, width=88)
```

## Contributing

To contribute to this project, check out our [contributing guide](CONTRIBUTING.md).

## Issues

If you run into an issue running a Markdown file, feel free to open an [issue][issues].
If you can include the faulting file, that will make it so much easier to debug.

This script can help in anonymizing your file if you have any confidential information
in it.

```python
#!/usr/bin/env python3
""" Anonymize file XXXX.md and output it to XXXX.out.md """
import pathlib
import random
import string

FILE_NAME = "XXXX.md"
input_path = pathlib.Path(FILE_NAME)
output_path = pathlib.Path(".out.".join(FILE_NAME.rsplit(".", maxsplit=1)))
text = input_path.read_text()
output = ""

for char in text:
    if char in string.ascii_lowercase:
        char = random.choice(string.ascii_lowercase)
    elif char in string.ascii_uppercase:
        char = random.choice(string.ascii_uppercase)
    output += char
output_path.write_text(output)
```

[issues]: https://github.com/duo-labs/markflow/issues

## Implementation

To read more about how to tool works, checkout the [implementation outline](
IMPLEMENTATION.md).

## Credits

This tool was inspired by a coworker not enjoying having to manually reformat Markdown
files. He wanted a tool that would enforce it for us like Python's [black][black]. That
is why the line length default is 88.

[black]: https://black.readthedocs.io/en/latest/

## A Bonus Note on Block Quote Formatting

Escaping `>` is especially important for the tool itself as otherwise updated block
quotes could be too deep. For instance, incorrect wrapping here could result in an extra
indented block of code.

```markdown
> Please don't wrap after this period. >
> Because I don't want to be a double quote.
```

becomes:

```markdown
> Please don't wrap after this period.
> > Because I don't want to be a
> double quote.
```

which would format to:

```markdown
> Please don't wrap after this period.
>> Because I don't want to be a
>> double quote.
```

Of course, if the tool tried that, it would throw an exception since it double checks
that if it were to be rerun the output would not change.
