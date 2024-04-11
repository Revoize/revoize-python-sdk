import pytest
from fixtures import cognito_client_id, cognito_region, password, username  # noqa: F401

from revoize import auth
from revoize.auth.exceptions import RevoizeAuthError


def test_login(username, password, cognito_client_id, cognito_region):  # noqa: F811
    login_result = auth.login(username, password, cognito_client_id, cognito_region)
    assert login_result.token is not None, "token not found in login result"


def test_invalid_login(username, cognito_client_id, cognito_region):  # noqa: F811
    with pytest.raises(RevoizeAuthError):
        auth.login(username, "invalid-password", cognito_client_id, cognito_region)
