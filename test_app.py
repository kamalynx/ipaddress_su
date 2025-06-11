from netaddr import valid_ipv6
from starlette.testclient import TestClient

from app import app


def test_app():
    client = TestClient(app, client=('::1', 8080))
    response = client.get('/')
    assert response.status_code == 200
    assert response.text == '::1'
    assert isinstance(response.text, str)
    assert valid_ipv6(response.text)
