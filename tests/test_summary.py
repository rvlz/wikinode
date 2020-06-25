import pytest

from wikinode import summary
from wikinode.exceptions import QueryAmbiguousError
from wikinode.requests import USER_AGENT
from tests.fixtures import (
    body,
    body_not_found,
    body_ambiguous,
    body_redirect,
)


@pytest.mark.parametrize("status_code,body", [(200, body)])
def test_fetch(response):
    """Test function can fetch one summary."""
    result = summary.fetch('"Hello, World!" program')
    # check HTTP request made correctly
    assert len(response.calls) == 1
    assert "redirect=true" in response.calls[0].request.url
    assert response.calls[0].request.headers["User-Agent"] == USER_AGENT
    # results
    assert set(result.keys()) == set(
        ["query", "title", "description", "extract"]
    )
    assert result["query"] == '"Hello, World!" program'
    assert result["title"] == body["title"]
    assert result["description"] == body["description"]
    assert result["extract"] == body["extract"]


@pytest.mark.parametrize("status_code,body", [(404, body_not_found)])
def test_fetch_no_article_found(response):
    """Test function returns empty dictionary when summary not found."""
    result = summary.fetch("hello123")
    # check HTTP request made correctly
    assert len(response.calls) == 1
    assert "redirect=true" in response.calls[0].request.url
    assert response.calls[0].request.headers["User-Agent"] == USER_AGENT
    # results
    assert result == {}


@pytest.mark.parametrize("status_code,body", [(200, body_ambiguous)])
def test_fetch_query_ambiguous(response):
    """Test function raises exception when query is not specific enough."""
    with pytest.raises(QueryAmbiguousError) as exc:
        summary.fetch("micro")
    assert "micro" in str(exc)
    # check HTTP request made correctly
    assert len(response.calls) == 1
    assert "redirect=true" in response.calls[0].request.url
    assert response.calls[0].request.headers["User-Agent"] == USER_AGENT


@pytest.mark.parametrize(
    "data",
    [[(302, "", {"Location": "Saint_Petersburg"}), (200, body_redirect, {})]],
)
def test_fetch_redirects(responses):
    """Test function can handle redirects."""
    result = summary.fetch("Leningrad")
    # check HTTP requests made correctly
    assert len(responses.calls) == 2
    assert "redirect=true" in responses.calls[0].request.url
    assert responses.calls[0].request.headers["User-Agent"] == USER_AGENT
    # results
    set(["query", "title", "description", "extract"])
    assert result["query"] == "Leningrad"
    assert result["title"] == body_redirect["title"]
    assert result["description"] == body_redirect["description"]
    assert result["extract"] == body_redirect["extract"]


@pytest.mark.parametrize(
    "data", [[(301, "", {"Location": "Hello_world"}), (200, body, {})]]
)
def test_fetch_permanent_redirects(responses):
    """Test function can handle permanent redirects."""
    result = summary.fetch("hello world")
    # check HTTP requests made correctly
    assert len(responses.calls) == 2
    assert "redirect=true" in responses.calls[0].request.url
    assert responses.calls[0].request.headers["User-Agent"] == USER_AGENT
    # results
    assert set(result.keys()) == set(
        ["query", "title", "description", "extract"]
    )
    assert result["query"] == "hello world"
    assert result["title"] == body["title"]
    assert result["description"] == body["description"]
    assert result["extract"] == body["extract"]


@pytest.mark.parametrize("status_code,body", [(200, body)])
def test_fetch_remove_extract_field(response):
    """Test 'extract' field removal from result."""
    result = summary.fetch('"Hello, World!" program', short=True)
    # check HTTP request made correctly
    assert len(response.calls) == 1
    assert "redirect=true" in response.calls[0].request.url
    assert response.calls[0].request.headers["User-Agent"] == USER_AGENT
    # results
    assert set(result.keys()) == set(["query", "title", "description"])
    assert result["query"] == '"Hello, World!" program'
    assert result["title"] == body["title"]
    assert result["description"] == body["description"]
