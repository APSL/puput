import pytest


@pytest.fixture
def site_url(request):
    return request.config.getoption("--site-url")


def pytest_addoption(parser):
    parser.addoption("--site-url", action="store", default="type1", help="url to test")
