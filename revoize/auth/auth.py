from typing import Optional

import requests

from ..defaults import DEFAULT_COGNITO_CLIENT_ID, DEFAULT_COGNITO_REGION
from ..schema import CognitoLoginResponse, Credentials
from .exceptions import NotAuthorizedException, RevoizeAuthError

COGNITO_AUTH_FLOW = "USER_PASSWORD_AUTH"


def login(
    username: str,
    password: str,
    cognito_client_id: Optional[str],
    cognito_region: Optional[str],
) -> Credentials:
    cognito_request_body = {
        "AuthParameters": {
            "USERNAME": username,
            "PASSWORD": password,
        },
        "AuthFlow": COGNITO_AUTH_FLOW,
        "ClientId": cognito_client_id or DEFAULT_COGNITO_CLIENT_ID,
    }
    # Source: https://stackoverflow.com/a/53343689/10243384
    headers = {
        "X-Amz-Target": "AWSCognitoIdentityProviderService.InitiateAuth",
        "Content-Type": "application/x-amz-json-1.1",
    }
    cognito_url = (
        f"https://cognito-idp.{cognito_region or DEFAULT_COGNITO_REGION}.amazonaws.com/"
    )

    response = requests.post(cognito_url, headers=headers, json=cognito_request_body)
    # TODO: Handle case where there is a challenge returned
    if response.ok:
        login_response = CognitoLoginResponse(**response.json())
        credentials = Credentials.from_cognito_login_response(login_response)
        return credentials
    else:
        try:
            response_body = response.json()
        except ValueError:
            raise RevoizeAuthError("Unknown error. Received invalid JSON body")
        if response_body["__type"] == "NotAuthorizedException":
            raise NotAuthorizedException("Invalid credentials")
        else:
            raise RevoizeAuthError("Unknown error")
