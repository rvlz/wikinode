import pytest

from wikinode import summary
from wikinode.exceptions import QueryAmbiguousError
from wikinode.requests import USER_AGENT, API_URL, RANDOM_SUMMARY_URL
from tests.fixtures import (
    body,
    body_not_found,
    body_ambiguous,
    body_redirect,
    fetch_results,
    fetch_results_ambiguous,
    fetch_results_not_found,
    fetch_results_mixed,
)


@pytest.mark.parametrize("status_code,body,url", [(200, body, API_URL)])
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


@pytest.mark.parametrize(
    "status_code,body,url", [(404, body_not_found, API_URL)]
)
def test_fetch_no_article_found(response):
    """Test function returns empty dictionary when summary not found."""
    result = summary.fetch("hello123")
    # check HTTP request made correctly
    assert len(response.calls) == 1
    assert "redirect=true" in response.calls[0].request.url
    assert response.calls[0].request.headers["User-Agent"] == USER_AGENT
    # results
    assert result == {}


@pytest.mark.parametrize(
    "status_code,body,url", [(200, body_ambiguous, API_URL)]
)
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
    [
        [
            (302, "", {"Location": "Saint_Petersburg"}, API_URL),
            (200, body_redirect, {}, API_URL),
        ]
    ],
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
    "data",
    [
        [
            (301, "", {"Location": "Hello_world"}, API_URL),
            (200, body, {}, API_URL),
        ]
    ],
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


@pytest.mark.parametrize("status_code,body,url", [(200, body, API_URL)])
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


def test_fetch_many(mocker):
    """Test function can fetch multiple summaries."""
    fetch_mock = mocker.patch("wikinode.summary.fetch")
    fetch_mock.side_effect = fetch_results
    queries = ["hello world", "python language", "Chicago"]
    results = summary.fetch_many(queries)
    # fetch assertions
    assert fetch_mock.call_count == 3
    fetch_mock.assert_any_call("hello world", short=False)
    fetch_mock.assert_any_call("python language", short=False)
    fetch_mock.assert_any_call("Chicago", short=False)
    # results
    assert results == fetch_results


def test_fetch_many_ambiguous_error(mocker):
    """
    Test function excludes queries that raise QueryAmbiguousError.
    """
    fetch_mock = mocker.patch("wikinode.summary.fetch")
    fetch_mock.side_effect = fetch_results_ambiguous
    # "micro" raises QueryAmbiguousError exception
    queries = ["hello world", "python language", "micro"]
    results = summary.fetch_many(queries)
    # fetch assertions
    assert fetch_mock.call_count == 3
    fetch_mock.assert_any_call("hello world", short=False)
    fetch_mock.assert_any_call("python language", short=False)
    fetch_mock.assert_any_call("micro", short=False)
    # results
    assert results == fetch_results_ambiguous[:-1]


def test_fetch_many_summary_not_found(mocker):
    """
    Test function excludes queries that weren't successful.
    """
    fetch_mock = mocker.patch("wikinode.summary.fetch")
    fetch_mock.side_effect = fetch_results_not_found
    # "hello123" fails
    queries = ["hello world", "python language", "hello123"]
    results = summary.fetch_many(queries)
    # fetch assertions
    assert fetch_mock.call_count == 3
    fetch_mock.assert_any_call("hello world", short=False)
    fetch_mock.assert_any_call("python language", short=False)
    fetch_mock.assert_any_call("hello123", short=False)
    # results
    assert results == fetch_results_not_found[:-1]


def test_fetch_many_remove_extract_field(mocker):
    """
    Test function excludes 'extract' fields from results.
    """
    fetch_mock = mocker.patch("wikinode.summary.fetch")
    queries = ["hello world", "python language", "Chicago"]
    summary.fetch_many(queries, short=True)
    # fetch assertions
    assert fetch_mock.call_count == 3
    fetch_mock.assert_any_call("hello world", short=True)
    fetch_mock.assert_any_call("python language", short=True)
    fetch_mock.assert_any_call("Chicago", short=True)


def test_fetch_many_with_meta_data(mocker):
    """
    Test function adds metadata about results.
    """
    fetch_mock = mocker.patch("wikinode.summary.fetch")
    fetch_mock.side_effect = fetch_results_mixed
    queries = [
        "hello world",
        "micro",
        "python language",
        "hello123",
        "Chicago",
    ]
    results = summary.fetch_many(queries, meta=True)
    assert fetch_mock.call_count == 5
    fetch_mock.assert_any_call("hello world", short=False)
    fetch_mock.assert_any_call("micro", short=False)
    fetch_mock.assert_any_call("python language", short=False)
    fetch_mock.assert_any_call("hello123", short=False)
    fetch_mock.assert_any_call("Chicago", short=False)
    assert results["hits"] == 3
    assert results["not_found"] == ["hello123"]
    assert results["ambiguous"] == ["micro"]
    assert results["results"] == [
        fetch_results_mixed[0],  # hello world
        fetch_results_mixed[2],  # python language
        fetch_results_mixed[4],  # Chicago
    ]


@pytest.mark.parametrize(
    "input",
    [
        2020,
        ["hello world"],
        {"query": "hello world"},
        ("hello world", "Chicago"),
    ],
)
def test_fetch_input(mocker, input):
    """Test fetch raises exception when query is not a string."""
    mocker.patch("wikinode.summary.requests.get")  # prevent HTTP real requests
    with pytest.raises(ValueError) as exc:
        summary.fetch(input)
    assert "Invalid argument. Argument must have type 'str'." in str(exc.value)


@pytest.mark.parametrize(
    "input",
    [
        2020,
        "hello world",
        {"query": "hello world"},
        ("hello world", "Chicago"),
    ],
)
def test_fetch_many_input(mocker, input):
    """Test fetch_many raises exception when query is not a list."""
    mocker.patch("wikinode.summary.fetch")
    with pytest.raises(ValueError) as exc:
        summary.fetch_many(input)
    assert "Invalid argument. Argument must have type 'list'." in str(
        exc.value
    )


@pytest.mark.parametrize(
    "status_code,body,url", [(200, body, RANDOM_SUMMARY_URL)]
)
def test_fetch_random(response):
    """Test function can fetch random article."""
    result = summary.fetch_random()
    # check HTTP request made correctly
    assert len(response.calls) == 1
    assert response.calls[0].request.headers["User-Agent"] == USER_AGENT
    # results
    assert set(result.keys()) == set(["title", "description", "extract"])
    assert result["title"] == body["title"]
    assert result["description"] == body["description"]
    assert result["extract"] == body["extract"]


@pytest.mark.parametrize(
    "status_code,body,url", [(404, body_not_found, RANDOM_SUMMARY_URL)]
)
def test_fetch_no_random_article_found(response):
    """Test function returns empty dictionary when summary not found."""
    result = summary.fetch_random()
    # check HTTP request made correctly
    assert len(response.calls) == 1
    assert response.calls[0].request.headers["User-Agent"] == USER_AGENT
    # results
    assert result == {}


@pytest.mark.parametrize(
    "status_code,body,url", [(200, body, RANDOM_SUMMARY_URL)]
)
def test_fetch_random_remove_extract_field(response):
    """Test 'extract' field removal from result."""
    result = summary.fetch_random(short=True)
    # check HTTP request made correctly
    assert len(response.calls) == 1
    assert response.calls[0].request.headers["User-Agent"] == USER_AGENT
    # results
    assert set(result.keys()) == set(["title", "description"])
    assert result["title"] == body["title"]
    assert result["description"] == body["description"]
