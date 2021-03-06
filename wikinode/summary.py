import requests

from wikinode.requests import (
    API_URL,
    RANDOM_SUMMARY_URL,
    USER_AGENT,
)
from wikinode.exceptions import QueryAmbiguousError


default_fields = ["title", "description", "extract"]


def _send_query(query):
    url = f"{API_URL}/{query}?redirect=true"
    response = requests.get(url, headers={"User-Agent": USER_AGENT})
    return response.json()


def _send_request(url):
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
    if not isinstance(query, str):
        raise ValueError("Invalid argument. Argument must have type 'str'.")
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


def fetch_many(queries, short=False, meta=False):
    """
    Request multiple summaries.

    Args:
        queries (list): A list of strings, each representing a single query.
        short (bool): Exclude the *extract* field from all successful results.
            By default, the 'extract' field is included.
        meta (bool): Include data about the batch of queries. The added keys
            include *hits* (number of successful queries), *not_found* (queries
            that have no corresponding article), and *ambiguous* (queries that
            have more than one corresponding article). The *results* key has
            the summary data.

    Returns:
        (list): Each result contains the fields *query*, *title*,
        *description*, and *extract*, which can be omitted.

    Example:

        >>> wikinode.fetch_many(["hello world", "python language"])
        [
          {
            'query': 'hello world',
            'title': '"Hello, World!" program',
            'description': "Traditional beginners' computer program",
            'extract': 'A "Hello, World!" program generally is a computer...'
          },
          {
            'query': 'python language',
            'title': 'Python (programming language)',
            'description': 'General-purpose, high-level programming language',
            'extract': 'Python is an interpreted, high-level, general...'
          }
        ]
        >>> queries = ["hello world", "python language", "123hello"]
        >>> wikinode.fetch_many(queries, meta=True)
        {
          'hits': 2,
          'not_found': ['123hello'],  # Couldn't find summary for "123hello"
          'ambiguous': [],  # no ambiguous query
          'results': [
            {
              'query': 'hello world',
              'title': '"Hello, World!" program',
              'description': "Traditional beginners' computer program",
              'extract': 'A "Hello, World!" program generally is a computer...'
            },
            {
              'query': 'python language',
              'title': 'Python (programming language)',
              'description': 'General-purpose, high-level programming...',
              'extract': 'Python is an interpreted, high-level, general...'
            }
          ]
        }
    """
    if not isinstance(queries, list):
        raise ValueError("Invalid argument. Argument must have type 'list'.")
    meta_data = {"hits": 0, "not_found": [], "ambiguous": []}
    results = []
    for query in queries:
        try:
            result = fetch(query, short=short)
        except QueryAmbiguousError:
            meta_data["ambiguous"].append(query)
            continue
        if result == {}:
            meta_data["not_found"].append(query)
            continue
        meta_data["hits"] += 1
        results.append(result)
    if meta:
        results = {**meta_data, "results": results}
    return results


def fetch_random(short=False):
    """
    Request a random summary.

    Args:
        short (bool): Exclude *extract* field from returned result.
            By default, the 'extract' field is included.
    Returns:
        (dict): Result contains the fields *title*, *description*,
        and *extract*, which can be omitted.

    Example:

        >>> wikinode.fetch_random()
        {
          'title': '"Hello, World!" program',
          'description': "Traditional beginners' computer program",
          'extract': 'A "Hello, World!" program generally is a computer...'
        }
        >>> wikinode.fetch_random(short=True)
        {
          'title': '"Hello, World!" program',
          'description': "Traditional beginners' computer program"
        }
    """
    data = _send_request(RANDOM_SUMMARY_URL)
    payload_type = data.get("type")
    if payload_type == "standard":
        summary = _select_subset(data)
        if short:
            del summary["extract"]
        return summary
    return {}
