class MarkdownFormatException(Exception):
    """ Raised if the passed in file is formatted incorrectly """


class ReformatInconsistentException(RuntimeError):
    """ Raised if a reformated Markdown file would be reformatted differently

    If you get this error, you should open a bug report.
    """
