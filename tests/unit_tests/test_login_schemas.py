from revoize.schema import CognitoLoginResponse, Credentials

TEST_AUTH_TOKEN = "test-auth-token"
TEST_DATA = {
    "AuthenticationResult": {
        "AccessToken": TEST_AUTH_TOKEN,
        "ExpiresIn": 86400,
        "IdToken": "test-id-token",
        "RefreshToken": "test-refresh-token",
        "TokenType": "Bearer",
    },
    # TODO: Improve handling of challenge parameters
    "ChallengeParameters": {},
}


def test_cognito_login_response_schema():
    test_value = CognitoLoginResponse(**TEST_DATA)
    assert test_value.authentication_result.access_token == TEST_AUTH_TOKEN


def test_credentials_schema():
    login_data = CognitoLoginResponse(**TEST_DATA)
    credentials = Credentials.from_cognito_login_response(login_data)
    assert credentials.token == TEST_AUTH_TOKEN


def test_as_auth_header():
    credentials = Credentials(token="test-token")
    auth_header = credentials.as_auth_header()
    assert "Authorization" in auth_header
    assert auth_header["Authorization"].startswith("Bearer ")
