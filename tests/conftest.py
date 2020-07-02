import re

import pytest
import responses as _responses


@pytest.fixture
def response(status_code, body, url):
    with _responses.RequestsMock() as rsps:
        rsps.add(
            _responses.GET,
            re.compile(f"^{url}"),
            json=body,
            status=status_code,
        )
        yield rsps


@pytest.fixture
def responses(data):
    with _responses.RequestsMock() as rsps:
        for status_code, body, headers, url in data:
            rsps.add(
                _responses.GET,
                re.compile(f"^{url}"),
                json=body,
                status=status_code,
                headers=headers,
            )
        yield rsps
