# markflow Behind Scenes

markflow is a pretty simple tool that formats code in three steps:

* [Parse the text](#parsing-markdown)
* [Reformat each section and stitch the sections back together](#reformatting-sections)
* [Rerun with the output as the input to guarantee consistency](#ensuring-consistency)

A potential future step, would be to render the text and ensure consistency outside of
some rules (see [Future Architecture Ideas](#future-architecture-ideas).

## Parsing Markdown

We parse markdown via a state machine that iterates over each line in some text. We
start in the default state which indicates to the machine we need to figure out what
type of section we just started seeing. At the beginning of each loop, we check to see
if whatever section we are in ended. This determination is configured each time we
change states.

## Reformatting Sections

The parsed text is gathered into a series of classes responsible for knowing how to
format different types of Markdown. The various enforced rules can be checked out in the
[README](README.md), but most implementations are fairly straightforward. More
complicated ones should be fairly well documented. (If you see one that is confusing,
open an issue.)

## Ensuring Consistency

Once everything is reformatted, that output is taken and then run through reformatting.
The two outputs are then compared to ensure consistency. This is important as the tool
provides a check so people can easily ensure their documents follow the formatting
rules.

## Future Architecture Ideas

Random ramblings on the future of markflow.

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
