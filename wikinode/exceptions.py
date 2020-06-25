"""wikinode exception classes."""


class QueryAmbiguousError(Exception):
    """
    Exception raised when query is not specific
    enough to return any meaningful data.
    """

    def __init__(self, query):
        self.query = query

    def __unicode__(self):
        return f'"{self.query}" not specific enough.'
