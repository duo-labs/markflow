# MarkFlow Behind Scenes

MarkFlow is a pretty simple tool that formats code in three steps:

* [Parse the text](#parsing-markdown)
* [Reformat each section and stitch the sections back together](#reformatting-sections)
* [Rerun with the output as the input to guarantee consistency](#ensuring-consistency)

A potential future step, would be to render the text and ensure consistency outside of
some rules (see [Future Architecture Ideas](#future-architecture-ideas).

## Parsing Markdown

We parse markdown by continuously iterating over a series of splitter functions. These
functions are designed per [CommonMark][commonmark_spec] section type. They take in a
string and if that string starts with their section type, they return a tuple of that
section and the remaining text. Otherwise, the return a None value for the first part of
the tuple and the entire part of the document as itself. Once we detect a section, we
break out and start over with the remaining text.

The functions are designed to be mutually exclusive: if one splitter splits the text, no
others will. This isn't really tested (hint, hint), but is hopefully achieved by
adhering to the [CommonMark][commonmark_spec] standard.

This means that we could endlessly iterate over the functions until no text is
remaining. But, if all of our splitters are incapable of processing the text, we end up
in an endless loop without extra tracking code. We also get the benefit of putting
resource intensive parsing later in the cycle so we only have to run it after we've
eliminated easier to parse sections.

[commonmark_spec]: https://spec.commonmark.org/0.29/

## Reformatting Sections

The parsed text is gathered into a series of classes responsible for knowing how to
format different types of Markdown. The various enforced rules can be checked out in the
[README](README.md), but most implementations are fairly straightforward. More
complicated ones should be fairly well documented. (If you see one that is confusing,
open an issue.)

<!-- ToDo: I think this should change to functions. I'm not sure what benefit we get
from having classes. -->

## Ensuring Consistency

Once everything is reformatted, that output is taken and then run through the parsing
and reformatting steps. The resulting document is then compared to our original
calculation to ensure they are the same. This allows us to be more confident that we
didn't mess up formatting since we calculate the same document structure between the
initial and resulting documents.

## Future Architecture Ideas

Random ramblings on the future of MarkFlow.

### Plugins

The tool supports tables but they are actually extensions and not a feature of the
[CommonMark][commonmark_spec] spec. Support for plugins could be added with tables being
the first adopter. This is likely not a big deal right now as there are probably not
many people making tables without necessary render extensions that wouldn't want to
still have them prettied up. Nor are people clamoring for support for other extensions
to the language.

[commonmark_spec]: https://spec.commonmark.org/0.29/

### Rendering Consistency

Another nice thing would be to enforce consistent rendering of the input files. Progress
on this has started as it is enforce by most tests, but since tables are an extension to
commonmark, the [library][commonmark_pkg]. A potential option that makes even more sense
in a plugin architecture would be having individual formatters handle validating
rendering consistency.

If you end up debugging an issue because of this, you can pass `--write-renders` to save
off the inputs. Pass `--dev-help` to see other developer options.

[commonmark_pkg]: https://github.com/readthedocs/commonmark.py
