import pytest
from fixtures import api_key

from revoize.api.client import RevoizeClient
from revoize.api.exceptions import RequestError


def test_get_user_info(api_key):
    client = RevoizeClient(api_key)
    user_info = client.get_user_info()
    assert user_info.id is not None


def test_invalid_api_key():
    client = RevoizeClient("invalid-key")
    with pytest.raises(RequestError):
        client.get_user_info()
