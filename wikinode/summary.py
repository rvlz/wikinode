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


def fetch(query):
    response = requests.get(
        f"{API_URL}/{query}?redirect=true", headers={"User-Agent": USER_AGENT},
    )
    if response.status_code == 404:
        return {}
    data = response.json()
    if data.get("type") == "disambiguation":
        raise QueryAmbiguousError(query)
    summary = _select_subset(data, meta={"query": query})
    return summary
