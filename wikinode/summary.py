import requests

from wikinode.requests import (
    API_URL,
    USER_AGENT,
)
from wikinode.exceptions import QueryAmbiguousError


default_fields = ["title", "description", "extract"]


def _select_subset(data, fields=default_fields, meta=None):
    subset = {k: data[k] for k in data if k in fields}
    if meta is not None:
        subset = {**subset, **meta}
    return subset


def fetch(query, short=False):
    """
    Request a single summary.

    Args:
        query (str): Search term to find an article summary.
        short (bool): Exclude *extract* field from returned result.
            By default, the 'extract' is included.

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
    response = requests.get(
        f"{API_URL}/{query}?redirect=true", headers={"User-Agent": USER_AGENT},
    )
    if response.status_code == 404:
        return {}
    data = response.json()
    if data.get("type") == "disambiguation":
        raise QueryAmbiguousError(query)
    fields = default_fields if not short else ["title", "description"]
    summary = _select_subset(data, fields=fields, meta={"query": query})
    return summary
