from datetime import timedelta

import pydantic

from revoize.api.utils import format_pydantic_error
from revoize.schema import UserInfo


def test_user_info_schema():
    # This is a mock for the response of the /users/me endpoint
    test_user_info_response = {
        "id": "test",
        "timeUsed": "PT12.820S",
        "userPlan": "BASIC",
    }
    value = UserInfo(**test_user_info_response)  # type: ignore
    assert isinstance(value.time_used, timedelta)
    assert value.time_used.total_seconds() == 12.820


def test_user_info_invalid_schema():
    test_user_info_response = {
        "id": "test",
        "timeUsed": "PT12.820S",
    }
    try:
        UserInfo(**test_user_info_response)  # type: ignore
    except pydantic.ValidationError as e:
        # Lax check, validate only that the missing parameter is mentioned
        assert "userPlan" in format_pydantic_error(e)
