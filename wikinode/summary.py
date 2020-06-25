import requests

from wikinode.requests import (
    API_URL,
    USER_AGENT,
)
from wikinode.exceptions import QueryAmbiguousError


default_fields = ["title", "description", "extract"]


def _send_query(query):
    url = f"{API_URL}/{query}?redirect=true"
    response = requests.get(url, headers={"User-Agent": USER_AGENT})
    return response.json()


def _select_subset(data, fields=default_fields, extra=None):
    subset = {k: data[k] for k in data if k in fields}
    if extra is not None:
        subset = {**subset, **extra}
    return subset


def fetch(query, short=False):
    """
    Request a single summary.

    Args:
        query (str): Search term to find an article summary.
        short (bool): Exclude *extract* field from returned result.
            By default, the 'extract' field is included.

    Returns:
        (dict): Result contains the fields *query*, *title*, *description*,
        and *extract*, which can be omitted.

    Raises:
        :py:class:`wikinode.exceptions.QueryAmbiguousError`
            If more than one article summary corresponds to the search term.

    Example:

        >>> wikinode.fetch("hello world")
        {
          'query': 'hello world',
          'title': '"Hello, World!" program',
          'description': "Traditional beginners' computer program",
          'extract': 'A "Hello, World!" program generally is a computer...'
        }
        >>> wikinode.fetch("hello world", short=True)
        {
          'query': 'hello world',
          'title': '"Hello, World!" program',
          'description': "Traditional beginners' computer program"
        }
    """
    data = _send_query(query)
    payload_type = data.get("type")
    summary = {}
    if payload_type == "standard":
        summary = _select_subset(data, extra={"query": query})
        if short:
            del summary["extract"]
    elif payload_type == "disambiguation":
        raise QueryAmbiguousError(query)
    return summary
