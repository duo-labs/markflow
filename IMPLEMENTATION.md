# MarkFlow Behind Scenes

MarkFlow is a pretty simple tool that formats code in three steps:

* [Parse the text](#parsing-markdown)
* [Reformat each section and stitch the sections back together](#reformatting-sections)
* [Rerun with the output as the input to guarantee consistency](#ensuring-consistency)

A potential future step would be to render the text and ensure consistency outside of
some rules (see [Future Architecture Ideas](#future-architecture-ideas)).

## Parsing Markdown

We parse **Markdown** by continuously iterating over a series of splitter functions.
Each function corresponds to a different [CommonMark][commonmark_spec] section type.
They take in a list of lines if that list starts with their section type, they return a
`tuple` of that section (as a `list` of lines) and the remaining text (also as a `list`
of lines). We use lists of lines as a performance gain, so we don't have to write (and
execute) `lst = str_.splitlines()` and `"\n".join(lst)` all over the place. Otherwise,
they return an empty `list` as the first member and the `list` of lines passed in as the
second. Once we detect a section, we continue parsing the remaining lines.

The functions are designed to be mutually exclusive: if one splitter splits the text, no
others should. This isn't really tested (hint, hint), but is hopefully achieved by
adhering to the [CommonMark][commonmark_spec] standard.

[commonmark_spec]: https://spec.commonmark.org/0.29/

## Reformatting Sections

The parsed text is then passed to the formatter class responsible for knowing how to
format its section type. The various enforced rules can be checked out in the [README](
README.md), but most implementations are fairly straightforward. More complicated ones
should be fairly well documented. (If you see one that is confusing, open an [issue][
issues].)

Some section types are recursive, namely lists and block quotes. These end up calling
back into the formatter again. We're not too worried about stack overflows since the
**Python** stack limit and the depth of recursive **Markdown** definitions by human
beings should different by several orders of magnitude (in favor of **Python**).

[issues]: https://github.com/duo-labs/markflow/issues

## Ensuring Consistency

Once everything is reformatted, that output is taken and then run through the parsing
and reformatting steps. The resulting document is then compared to our original
calculation to ensure they are the same. This allows us to be more confident that we
didn't mess up formatting since we calculate the same document structure between the
initial and resulting documents.

## Future Architecture Ideas

Here are some of random ramblings on the future of **MarkFlow**.

### Plugins

The tool supports tables, but they are actually extensions and not a feature of the
[CommonMark][commonmark_spec] spec. Support for plugins could be added with tables being
the first adopter. This is likely not a big deal right now as there are probably not
many people making tables without necessary render extensions that wouldn't want to
still have them prettied up. Nor are people clamoring for support for other extensions
to the language.

[commonmark_spec]: https://spec.commonmark.org/0.29/

### Rendering Consistency

Another nice thing would be to enforce consistent rendering of the input files. Progress
on this has started as it is enforced by most tests, but tables are an extension to
CommonMark and not a part of the library itself, and the [CommonMark validation
library][commonmark_pkg] we are using don't support them. A potential option that makes
even more sense in a plugin architecture would be having individual formatters handle
validating rendering consistency.

If you end up debugging an issue because of this, you can pass `--write-renders` to save
off the inputs. Pass `--dev-help` to see other developer options, if you're curious.

[commonmark_pkg]: https://github.com/readthedocs/commonmark.py
