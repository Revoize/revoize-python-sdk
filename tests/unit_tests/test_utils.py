import pytest
from pydantic import BaseModel
from pytest_mock import MockerFixture

from revoize.api.exceptions import InvalidResponseSchema, RequestError
from revoize.api.utils import raise_if_response_not_ok, try_parse_response


def test_try_parse_response(mocker: MockerFixture):
    response = mocker.Mock()

    class TestModel(BaseModel):
        test: str

    response.json.return_value = {"test": "value"}
    result = try_parse_response(response, TestModel)
    assert isinstance(result, TestModel)


def test_try_parse_response_fails(mocker: MockerFixture):
    response = mocker.Mock()

    class TestModel(BaseModel):
        test: str

    response.json.return_value = {"test": 1234}
    with pytest.raises(InvalidResponseSchema):
        try_parse_response(response, TestModel)


def test_raise_if_response_not_ok(mocker: MockerFixture):
    response = mocker.Mock()
    response.ok = False
    response.status_code = 500
    response.text = "Test response"
    test_error_message = "Test Error"
    with pytest.raises(RequestError) as error_info:
        raise_if_response_not_ok(response, test_error_message)
    assert test_error_message in str(error_info.value)
    assert response.text in str(error_info.value)
    assert str(response.status_code) in str(error_info.value)
