import re

import pytest
import responses as _responses

from wikinode.requests import API_URL


@pytest.fixture
def response(status_code, body):
    with _responses.RequestsMock() as rsps:
        rsps.add(
            _responses.GET,
            re.compile(f"^{API_URL}"),
            json=body,
            status=status_code,
        )
        yield rsps


@pytest.fixture
def responses(data):
    with _responses.RequestsMock() as rsps:
        for status_code, body, headers in data:
            rsps.add(
                _responses.GET,
                re.compile(f"^{API_URL}"),
                json=body,
                status=status_code,
                headers=headers,
            )
        yield rsps
